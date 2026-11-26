You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: SubscribeToTask and CancelTask bypass owner-aware TaskStore for live tasks

### What happened?

`DefaultRequestHandlerV2.on_subscribe_to_task` and `on_cancel_task` resolve the task through `ActiveTaskRegistry` by `task_id` alone. `get_or_create()` returns the cached `ActiveTask` before the owner-aware `TaskStore` is consulted, so a caller other than the task owner can subscribe to and cancel another user's live task.

Owner isolation itself works: `GetTask` and `SendMessage` consult `task_store.get(task_id, context)` first and correctly raise `TaskNotFoundError`. Only the two registry-backed paths skip it, so behaviour is inconsistent across request paths. This narrows the task-authorization half of #786, which predates owner-aware stores and `resolve_user_scope`.

Practical exploitability is low: `task_id` defaults to `uuid4()`, so it cannot be guessed or enumerated — the caller must already know the id.

**Expected:** `SubscribeToTask` / `CancelTask` for a task outside the caller's partition raise `TaskNotFoundError`, the same response as for a nonexistent task.

**Actual:** the call succeeds. The subscriber receives the owner's `Task` and event stream; `CancelTask` cancels the task and invokes `AgentExecutor.cancel()`.

**Affected:** a2a-sdk 1.1.2 (latest) and current `main`.

**Root cause**

- `active_task_registry.py:52-53` — `get_or_create()` returns `self._active_tasks[task_id]` with no owner check; `call_context` is not consulted on that path.
- `default_request_handler_v2.py:169` (`on_cancel_task`) and `:398` (`on_subscribe_to_task`) call `get_or_create()` without a prior `task_store.get(task_id, context)`. `_setup_active_task` does perform it (`:203`), which is why `SendMessage` is unaffected.

Preconditions: the task must still be live (present in `ActiveTaskRegistry`) and the caller must know its `task_id`. Tasks that are no longer active are isolated correctly.

**Side effect:** `ActiveTask.cancel()` assigns the caller's context to `TaskManager._call_context` (`active_task.py:718`), so the cancelled task is additionally persisted into the caller's store partition.

**Reproduction** — Python 3.13, `pip install a2a-sdk==1.1.2` (no extras):

```python
"""Minimal reproduction: owner-isolation bypass for live tasks in a2a-sdk 1.1.2.

`SubscribeToTask` and `CancelTask` resolve the task through `ActiveTaskRegistry`
by `task_id` alone. The registry returns the cached `ActiveTask` before the
owner-aware `TaskStore` is ever consulted, so any authenticated caller can read
another user's in-flight task stream and cancel that task.

`SendMessage` is not affected: `_setup_active_task` performs an owner-aware
`task_store.get()` first.

Run: python repro_owner_isolation.py
"""

import asyncio
import logging

from a2a.auth.user import User
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.context import ServerCallContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandlerV2
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types.a2a_pb2 import (
    AgentCapabilities,
    AgentCard,
    CancelTaskRequest,
    GetTaskRequest,
    Message,
    Part,
    Role,
    SendMessageConfiguration,
    SendMessageRequest,
    SubscribeToTaskRequest,
    Task,
    TaskState,
    TaskStatus,
)


# Unrelated teardown noise from the event queue would otherwise mix into the output.
logging.getLogger('a2a').setLevel(logging.ERROR)


class NamedUser(User):
    """Authenticated user whose name is the owner key of the default resolver."""

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def user_name(self) -> str:
        return self._name


class LongRunningAgent(AgentExecutor):
    """Agent that stays in `working` state so the task remains live."""

    def __init__(self) -> None:
        self.working = asyncio.Event()
        self.cancel_called = asyncio.Event()

    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        await event_queue.enqueue_event(
            Task(
                id=context.task_id,
                context_id=context.context_id,
                status=TaskStatus(state=TaskState.TASK_STATE_SUBMITTED),
            )
        )
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.start_work()
        self.working.set()
        await asyncio.sleep(3600)

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        self.cancel_called.set()
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        await updater.cancel()


def user_message(text: str) -> Message:
    return Message(
        message_id=f'msg-{text}',
        role=Role.ROLE_USER,
        parts=[Part(text=text)],
    )


async def main() -> None:
    agent = LongRunningAgent()
    store = InMemoryTaskStore()
    handler = DefaultRequestHandlerV2(
        agent_executor=agent,
        task_store=store,
        agent_card=AgentCard(capabilities=AgentCapabilities(streaming=True)),
    )

    alice = ServerCallContext(user=NamedUser('alice'))
    bob = ServerCallContext(user=NamedUser('bob'))

    # Alice starts a long-running task; the producer keeps running in the
    # background after the HTTP response, so the task stays in the registry.
    alice_task = await handler.on_message_send(
        SendMessageRequest(
            message=user_message('alice-work'),
            configuration=SendMessageConfiguration(return_immediately=True),
        ),
        alice,
    )
    task_id = alice_task.id
    await asyncio.wait_for(agent.working.wait(), timeout=5)
    print(f"Alice's live task: {task_id} state={TaskState.Name(alice_task.status.state)}")

    # Control: every path that consults the owner-aware store first is isolated.
    print('\n[control] store.get() as Bob ->', await store.get(task_id, bob))
    try:
        await handler.on_get_task(GetTaskRequest(id=task_id), bob)
        print('[control] GetTask as Bob -> returned a task (unexpected)')
    except Exception as exc:  # noqa: BLE001
        print(f'[control] GetTask as Bob -> {type(exc).__name__} (isolated)')
    try:
        await handler.on_message_send(
            SendMessageRequest(
                message=Message(
                    message_id='bob-followup',
                    role=Role.ROLE_USER,
                    parts=[Part(text='hijack')],
                    task_id=task_id,
                ),
                configuration=SendMessageConfiguration(return_immediately=True),
            ),
            bob,
        )
        print('[control] SendMessage on Alice\'s task as Bob -> accepted (unexpected)')
    except Exception as exc:  # noqa: BLE001
        print(
            f"[control] SendMessage on Alice's task as Bob -> "
            f'{type(exc).__name__} (isolated)'
        )

    # Bug 1: Bob subscribes to Alice's live task and receives her task state.
    stream = handler.on_subscribe_to_task(SubscribeToTaskRequest(id=task_id), bob)
    first_event = await asyncio.wait_for(anext(stream), timeout=5)
    print(
        f'\n[BUG 1] SubscribeToTask as Bob -> {type(first_event).__name__} '
        f'id={getattr(first_event, "id", None)} '
        f'(Alice\'s task: {getattr(first_event, "id", None) == task_id})'
    )
    await stream.aclose()

    # Bug 2: Bob cancels Alice's live task.
    cancelled = await handler.on_cancel_task(CancelTaskRequest(id=task_id), bob)
    print(
        f'[BUG 2] CancelTask as Bob -> state='
        f'{TaskState.Name(cancelled.status.state)} '
        f'agent.cancel() called={agent.cancel_called.is_set()}'
    )

    # Side effect: ActiveTask.cancel() overwrites TaskManager._call_context with
    # the caller's context (active_task.py:718), so the cancelled task is also
    # persisted into Bob's partition — Bob now owns a copy of Alice's task.
    print(
        '\n[side effect] store.get() as Bob   ->',
        (await store.get(task_id, bob)) is not None,
    )
    print(
        '[side effect] store.get() as Alice ->',
        (await store.get(task_id, alice)) is not None,
    )

    await handler.aclose()


if __name__ == '__main__':
    asyncio.run(main())
```

The three control checks in the script confirm the owner-aware store isolates users correctly; only the two registry-backed paths bypass it.

**Suggested fix:** consult the owner-aware store before returning a cached `ActiveTask` — either in the two handler methods or inside `get_or_create()` — and raise `TaskNotFoundError` when the task is not in the caller's partition, so existence is not leaked. Optionally, leave `TaskManager._call_context` untouched in `ActiveTask.cancel()`.

### Relevant log output

```shell
Alice's live task: afff69f4-eef4-499f-8c99-e1cc4eb45644 state=TASK_STATE_SUBMITTED

[control] store.get() as Bob -> None
[control] GetTask as Bob -> TaskNotFoundError (isolated)
[control] SendMessage on Alice's task as Bob -> TaskNotFoundError (isolated)

[BUG 1] SubscribeToTask as Bob -> Task id=afff69f4-eef4-499f-8c99-e1cc4eb45644 (Alice's task: True)
[BUG 2] CancelTask as Bob -> state=TASK_STATE_CANCELED agent.cancel() called=True

[side effect] store.get() as Bob   -> True
[side effect] store.get() as Alice -> True
```

### Code of Conduct

- [X] I agree to follow this project's Code of Conduct

