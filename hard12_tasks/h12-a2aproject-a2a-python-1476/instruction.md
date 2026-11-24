You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: JSON-RPC client ignores the JSON-RPC error body when the HTTP status is not 2xx

### What happened?

`JsonRpcTransport` raises the mapped A2A error for a JSON-RPC error response only when the HTTP status is 2xx. If a server sends the same error body with a non-2xx status, the client raises a generic `A2AClientError("HTTP Error 500: ...")`. The JSON-RPC error code and the server's message are lost.

a2a-js does this. Errors raised outside its main handler (the user builder, the agent card lookup) that map to `-32603` are sent as HTTP 500 with a normal JSON-RPC error body ([json_rpc_handler.ts#L219-L220](https://github.com/a2aproject/a2a-js/blob/41335e66b6941db20065580782b909ff6e8476c0/src/server/express/json_rpc_handler.ts#L219-L220)). Section 9.5 of the spec defines the error object, not the HTTP status, so the client can't assume 200. `RestTransport` already reads the error body on non-2xx responses (`_handle_http_error`).

To reproduce on `main` (caab6a2):

```python
import asyncio

import httpx

from a2a.client.transports.jsonrpc import JsonRpcTransport
from a2a.types.a2a_pb2 import AgentCard, GetTaskRequest

BODY = {
    'jsonrpc': '2.0',
    'id': '1',
    'error': {'code': -32603, 'message': 'database connection lost'},
}


async def main(status: int) -> None:
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(status, json=BODY)
        )
    )
    transport = JsonRpcTransport(client, AgentCard(), 'http://agent')
    try:
        await transport.get_task(GetTaskRequest(id='t1'))
    except Exception as e:
        print(f'HTTP {status}: {type(e).__name__}: {e}')


asyncio.run(main(200))
asyncio.run(main(500))
```

Expected: both calls raise `InternalError: database connection lost`.

Actual: the HTTP 500 call raises `A2AClientError: HTTP Error 500: ...`. `send_message_streaming` and `subscribe` behave the same way: a 404 whose body is a `-32001` error raises `A2AClientError` instead of `TaskNotFoundError`.

Root cause: `_send_request` and `_send_stream_request` pass no `status_error_handler` to the shared HTTP helpers ([jsonrpc.py#L319-L330](https://github.com/a2aproject/a2a-python/blob/caab6a252958b2218ea61c0cae772f0a5c159e2a/src/a2a/client/transports/jsonrpc.py#L319-L330), [jsonrpc.py#L368-L376](https://github.com/a2aproject/a2a-python/blob/caab6a252958b2218ea61c0cae772f0a5c159e2a/src/a2a/client/transports/jsonrpc.py#L368-L376)), so `handle_http_exceptions` raises without reading the body.

Proposed fix: give `JsonRpcTransport` a status error handler, like `RestTransport._handle_http_error`. If the body is a JSON-RPC error object, raise the mapped error. Otherwise keep the current `A2AClientError("HTTP Error ...")`, so HTML pages from proxies and other non-JSON-RPC bodies behave as today.

One behaviour change to flag: code that catches `A2AClientError` for these responses would get the mapped `A2AError` subclass instead (`InternalError` is not an `A2AClientError`). That's already what happens for the same body at HTTP 200, and what `RestTransport` does. `except A2AError` is unaffected.

I'm happy to open a PR for this.

### Relevant log output

```shell
HTTP 200: InternalError: database connection lost
HTTP 500: A2AClientError: HTTP Error 500: Server error '500 Internal Server Error' for url 'http://agent'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500
```

