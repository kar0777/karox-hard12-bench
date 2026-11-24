You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: v0.3 REST client puts raw task and push config ids in URL paths, so ids with # or ? read the wrong resource

### What happened?

#1436 made `RestTransport` percent-encode task ids and push config ids in URL paths. `CompatRestTransport` (the v0.3 REST client) still puts them in the path as raw text, so an id containing `#`, `?` or `%` reaches a different resource.

Paths built from raw ids on `main` (2ba8e7b):
- `get_task`: https://github.com/a2aproject/a2a-python/blob/2ba8e7bd27fce7de92c33813a46dbea1e3f7e6ce/src/a2a/compat/v0_3/rest_transport.py#L166
- `cancel_task`: https://github.com/a2aproject/a2a-python/blob/2ba8e7bd27fce7de92c33813a46dbea1e3f7e6ce/src/a2a/compat/v0_3/rest_transport.py#L195
- push config create / get / list: https://github.com/a2aproject/a2a-python/blob/2ba8e7bd27fce7de92c33813a46dbea1e3f7e6ce/src/a2a/compat/v0_3/rest_transport.py#L224-L267
- `subscribe`: https://github.com/a2aproject/a2a-python/blob/2ba8e7bd27fce7de92c33813a46dbea1e3f7e6ce/src/a2a/compat/v0_3/rest_transport.py#L311

**Repro.** A real `DefaultRequestHandler` behind `create_rest_routes(..., enable_v0_3_compat=True)`, called through `httpx.ASGITransport`. The same calls go through both clients:

```python
import asyncio, httpx
from starlette.applications import Starlette
from a2a.client.transports.rest import RestTransport
from a2a.compat.v0_3.rest_transport import CompatRestTransport
from a2a.server.context import ServerCallContext
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_rest_routes
from a2a.server.tasks import InMemoryPushNotificationConfigStore, InMemoryTaskStore
from a2a.types.a2a_pb2 import (
    AgentCapabilities, AgentCard, GetTaskPushNotificationConfigRequest,
    GetTaskRequest, Task, TaskPushNotificationConfig, TaskState, TaskStatus,
)

async def main():
    store = InMemoryTaskStore()
    await store.save(Task(id='t1', context_id='c1', status=TaskStatus(state=TaskState.TASK_STATE_WORKING)), ServerCallContext())
    card = AgentCard(capabilities=AgentCapabilities(push_notifications=True))
    handler = DefaultRequestHandler(None, store, card, push_config_store=InMemoryPushNotificationConfigStore())
    app = Starlette(routes=create_rest_routes(request_handler=handler, enable_v0_3_compat=True))
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), headers={'A2A-Version': '1.0'}) as hc:
        for name, t in [('RestTransport', RestTransport(hc, card, 'http://agent')),
                        ('CompatRestTransport', CompatRestTransport(hc, card, 'http://agent'))]:
            for cid, url in [('alerts', 'https://hooks.example.com/alerts'), ('alerts#ops', 'https://hooks.example.com/ops')]:
                await t.create_task_push_notification_config(TaskPushNotificationConfig(task_id='t1', id=cid, url=url))
            got = await t.get_task_push_notification_config(GetTaskPushNotificationConfigRequest(task_id='t1', id='alerts#ops'))
            print(f'{name}: get config "alerts#ops" -> id={got.id!r}')
            try:
                task = await t.get_task(GetTaskRequest(id='t1?x'))
                print(f'{name}: get_task("t1?x") -> task {task.id!r}')
            except Exception as e:
                print(f'{name}: get_task("t1?x") -> {type(e).__name__}')

asyncio.run(main())
```

Output on `main`:

```
RestTransport: get config "alerts#ops" -> id='alerts#ops'
RestTransport: get_task("t1?x") -> TaskNotFoundError
CompatRestTransport: get config "alerts#ops" -> id='alerts'
CompatRestTransport: get_task("t1?x") -> task 't1'
```

**Expected:** the v0.3 client reaches the resource it names, like `RestTransport` does now: `alerts#ops` returns the `alerts#ops` config, and `t1?x` is not found.

**Actual:** `#ops` becomes a URL fragment and `?x` a query string, so the v0.3 client returns the config `alerts` and the task `t1`.

The fix is the same `quote(value, safe='')` that #1436 applied, at the six path sites above.

I have a fix with a regression test and will open a PR.

### Code of Conduct

- [x] I agree to follow this project's Code of Conduct

