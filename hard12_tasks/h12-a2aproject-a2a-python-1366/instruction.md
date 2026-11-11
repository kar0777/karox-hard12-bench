You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: Executor failure right after its Task is enqueued leaves the task SUBMITTED on DatabaseTaskStore

Follow-up to #1067, on a path #1106 did not cover.

### What happened?

With `DatabaseTaskStore`, if an executor enqueues its `Task` and raises before that Task is saved, the failure write that #1106 added to `_run_producer` races the consumer's save of the Task. Both insert the same row and one of them fails:

- If the producer's insert fails, the error never reaches the consumer. `on_message_send` returns the task as `SUBMITTED`, and the row stays `SUBMITTED`.
- If the consumer's insert fails, `on_message_send` raises `IntegrityError` instead of the executor's error, and the stored task is the fallback, without the agent's metadata.

The window is about one store write, so it hits fast failures such as a refused connection, missing credentials or input validation, not failures after a model call. `InMemoryTaskStore` is not affected because its save never yields. Same on v1.2.2.

### Reproduction

<details>
<summary>repro.py</summary>

```python
import asyncio
import collections
import tempfile
import uuid

from sqlalchemy.ext.asyncio import create_async_engine

from a2a.helpers.proto_helpers import new_task_from_user_message
from a2a.server.agent_execution import AgentExecutor
from a2a.server.context import ServerCallContext
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks.database_task_store import DatabaseTaskStore
from a2a.types.a2a_pb2 import AgentCard, Message, Part, Role, SendMessageRequest, TaskState


class FailsAfterCreatingTask(AgentExecutor):
    async def execute(self, context, event_queue):
        task = new_task_from_user_message(context.message)
        task.metadata.update({'agent_key': 'kept'})
        self.task_id = task.id
        await event_queue.enqueue_event(task)
        raise RuntimeError('model call failed')

    async def cancel(self, context, event_queue):
        pass


async def main():
    engine = create_async_engine(f'sqlite+aiosqlite:///{tempfile.mkdtemp()}/tasks.db')
    store = DatabaseTaskStore(engine)
    executor = FailsAfterCreatingTask()
    handler = DefaultRequestHandler(executor, store, AgentCard(name='repro'))
    outcomes = collections.Counter()
    for _ in range(50):
        message = Message(role=Role.ROLE_USER, message_id=str(uuid.uuid4()), parts=[Part(text='hi')])
        context = ServerCallContext()
        try:
            result = await handler.on_message_send(SendMessageRequest(message=message), context)
            client = f'returned {TaskState.Name(result.status.state)}'
        except Exception as exc:
            client = f'raised {type(exc).__name__}'
        await asyncio.sleep(0.1)
        stored = await store.get(executor.task_id, context)
        kept = 'agent_key' in stored.metadata
        outcomes[(client, TaskState.Name(stored.status.state), kept)] += 1
    for (client, state, kept), n in outcomes.most_common():
        print(f'{n:3}  {client:30} stored {state:21} metadata kept: {kept}')


asyncio.run(main())
```

</details>

On `main` (01da00b), none of the 50 runs ends with the executor's error and a FAILED task:

```text
 30  returned TASK_STATE_SUBMITTED  stored TASK_STATE_SUBMITTED  metadata kept: True
 19  raised IntegrityError          stored TASK_STATE_FAILED     metadata kept: False
  1  raised RuntimeError            stored TASK_STATE_FAILED     metadata kept: False
```

### Proposed fix

Make the consumer the only writer. The producer enqueues the failure instead of writing it, and the consumer writes FAILED after the events the executor enqueued before raising, creating the fallback task only if the executor never made one. An upsert in `DatabaseTaskStore.save` fixes the state but lets the fallback overwrite the agent's Task, and a lock still drops the agent's Task when the producer gets there first.

I have the change with a regression test that fails on `main` and passes with it, and can open a PR.

### Environment

a2a-sdk `main` @ 01da00b and v1.2.2, Python 3.12, SQLAlchemy 2.1.5, aiosqlite 0.22.1, Linux.

