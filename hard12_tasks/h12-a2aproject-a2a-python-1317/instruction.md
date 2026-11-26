You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: DefaultRequestHandler runs follow-up messages on a task with the first request's contextvars

### What happened?

With `DefaultRequestHandler` (v2), a follow-up message on an existing task runs `AgentExecutor.execute()` with the contextvars of the request that **created** the task, not the request that sent the follow-up. A common case is a reply after the task went `input-required`.

Any per-request contextvar set by ASGI middleware or by the `ServerCallContextBuilder` comes through stale: auth tokens, tenant or caller identity, request-scoped tracing. `ServerCallContext.state` is correct per message. Only contextvars are wrong.

Reproduced on 1.1.2 and 1.2.2, for both `SendMessage` and `SendStreamingMessage`. 0.3.x is not affected because its handler started a new producer per message.

### Cause

`ActiveTask.start()` creates the producer with `asyncio.create_task(self._run_producer())` during the first request, so the producer copies that request's context once. Later requests call `ActiveTask.enqueue_request()`, which only puts the `RequestContext` on `_request_queue`. The producer then calls `execute()` from the first request's context. A task parked in `input-required` keeps its `ActiveTask` (#1296), so a reply hours later still sees the first request's values, which may by then be an expired token.

### Reproduction

```python
import asyncio, contextvars, uuid

import httpx
from a2a.helpers import new_task_from_user_message
from a2a.server.agent_execution import AgentExecutor
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import AgentCapabilities, AgentCard
from starlette.applications import Starlette

REQUEST_TAG = contextvars.ContextVar("request_tag", default="unset")


class TagMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        token = REQUEST_TAG.set(dict(scope.get("headers", [])).get(b"x-tag", b"unset").decode())
        try:
            await self.app(scope, receive, send)
        finally:
            REQUEST_TAG.reset(token)


class Executor(AgentExecutor):
    async def execute(self, context, event_queue):
        print(f"execute({context.get_user_input()!r}) sees request_tag={REQUEST_TAG.get()!r}")
        task = context.current_task or new_task_from_user_message(context.message)
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        if context.current_task:
            await updater.complete()
        else:
            await event_queue.enqueue_event(task)
            await updater.requires_input()

    async def cancel(self, context, event_queue):
        pass


card = AgentCard(name="a", description="a", version="1", capabilities=AgentCapabilities())
handler = DefaultRequestHandler(agent_executor=Executor(), task_store=InMemoryTaskStore(), agent_card=card)
app = Starlette(routes=create_jsonrpc_routes(request_handler=handler, rpc_url="/"))
app.add_middleware(TagMiddleware)


async def send(client, tag, text, task=None):
    message = {"messageId": str(uuid.uuid4()), "role": "ROLE_USER", "parts": [{"text": text}]}
    if task:
        message |= {"taskId": task["id"], "contextId": task["contextId"]}
    body = {"jsonrpc": "2.0", "id": 1, "method": "SendMessage", "params": {"message": message}}
    resp = await client.post("/", json=body, headers={"x-tag": tag, "A2A-Version": "1.0"})
    return resp.json()["result"]["task"]


async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t") as client:
        task = await send(client, "request-1", "book a flight")
        await send(client, "request-2", "Friday", task)


asyncio.run(main())
```

Actual:

```
execute('book a flight') sees request_tag='request-1'
execute('Friday') sees request_tag='request-1'
```

Expected:

```
execute('book a flight') sees request_tag='request-1'
execute('Friday') sees request_tag='request-2'
```

### Proposed fix

Capture the sender's context in `enqueue_request()` and run `execute()` in it:

```python
async def enqueue_request(self, request_context):
    request_id = uuid.uuid4()
    await self._request_queue.put((request_context, request_id, contextvars.copy_context()))
    return request_id

# in _run_producer()
request_context, request_id, sender_context = await self._request_queue.get()
...
await sender_context.run(
    asyncio.create_task,
    self._agent_executor.execute(request_context, self._event_queue_agent),
)
```

I applied this patch to 1.2.2 locally and the reproduction prints `request-2` for the follow-up, for both `SendMessage` and `SendStreamingMessage`. `Context.run(asyncio.create_task, ...)` works on Python 3.10. Awaiting the child task keeps cancellation working, because cancelling the producer cancels the child. The MCP Python SDK fixed the same problem this way in modelcontextprotocol/python-sdk#2298.

### Downstream workaround

bedrock-agentcore works around this today without touching a2a internals. It wraps `SimpleRequestContextBuilder` to store `contextvars.copy_context()` in `call_context.state`, and wraps the executor to run `execute()` in that copy (aws/bedrock-agentcore-sdk-python#690). A fix here would let downstream projects delete that code, and it would also cover users who build `DefaultRequestHandler` directly.

### Relevant log output

_No response_

### Code of Conduct

- [x] I agree to follow this project's Code of Conduct

