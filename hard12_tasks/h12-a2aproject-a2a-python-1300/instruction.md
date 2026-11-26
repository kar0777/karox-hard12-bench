You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: REST client raises AttributeError when an HTTP error body is not a google.rpc.Status

### What happened?

When a REST call fails with an HTTP error whose JSON body is not a `google.rpc.Status` object, `RestTransport` raises a bare `AttributeError` instead of an A2A client error. This is common when the response comes from a proxy or gateway rather than the agent, e.g. an OAuth layer answering `401` with `{"error": "invalid_token"}` (RFC 6750), or a load balancer answering `502` with a JSON string.

`_parse_rest_error` (`src/a2a/client/transports/rest.py`) assumes `payload["error"]` is an object:

```python
error_data = error_payload.get('error', {})
message = error_data.get('message', fallback_message)  # str / list / None -> AttributeError
```

`_handle_http_error` only catches `JSONDecodeError`/`ValueError`, so the status-based fallback below it (`MethodNotFoundError` for 404, `A2AClientError` otherwise) never runs. Streaming calls fail the same way. The v0.3 compat REST transport has the same problem in its `_handle_http_error` (`error_data.get('type')` on a non-object body).

### Reproduction (main @ dac7d9d)

```python
import asyncio, httpx
from a2a.client.transports.rest import RestTransport
from a2a.types.a2a_pb2 import AgentCard, GetTaskRequest

async def main():
    client = httpx.AsyncClient(transport=httpx.MockTransport(
        lambda r: httpx.Response(401, json={"error": "invalid_token"})))
    await RestTransport(client, AgentCard(), "http://agent").get_task(GetTaskRequest(id="t1"))

asyncio.run(main())
# AttributeError: 'str' object has no attribute 'get'
```

| Status | Body | Raised | Expected |
|---|---|---|---|
| 401 | `{"error": "invalid_token"}` | `AttributeError` | `A2AClientError` |
| 404 | `{"error": "Not Found"}` | `AttributeError` | `MethodNotFoundError` |
| 502 | `["bad gateway"]` | `AttributeError` | `A2AClientError` |
| 500 | `"Internal Server Error"` | `AttributeError` | `A2AClientError` |
| 503 | `null` | `AttributeError` | `A2AClientError` |

A well-formed `google.rpc.Status` body still maps correctly (e.g. `TASK_NOT_FOUND` → `TaskNotFoundError`).

### Expected

Bodies that are not a `google.rpc.Status` are ignored, and the existing HTTP-status fallback applies. I have a small fix with regression tests ready and will open a PR.

