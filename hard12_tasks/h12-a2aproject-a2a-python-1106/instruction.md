You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: ActiveTaskRegistry.get_or_create produces orphan SUBMITTED rows on early _run_producer exception

### What happened?

In long-running production deployments using `DefaultRequestHandlerV2` + `DatabaseTaskStore`, a small but non-zero fraction of tasks end up persisted as **orphan rows**:

- `status.state == TaskState.TASK_STATE_SUBMITTED`
- `history == []` (empty)
- `metadata == None`
- `last_updated == None`
- The task never transitions out of `SUBMITTED`; no further updates are ever written.

Observed rate: roughly **1 orphan per 80-170 tasks** across multiple long-running agent processes (a2a-sdk 1.0.3). Latest `main` (commit on HEAD at time of filing) is also affected — the relevant code paths are unchanged.

These rows accumulate indefinitely in the task store. Downstream consumers (resume flows, list-tasks UIs, queue-depth heuristics) need defensive filtering to avoid treating them as live work.

### Root cause

The orphan is produced by a race between `ActiveTaskRegistry.get_or_create()` and the `_run_producer` exception path:

1. `ActiveTaskRegistry.get_or_create()` (in `src/a2a/server/agent_execution/active_task_registry.py`) constructs a `TaskManager` with `initial_message=None`:

   ```python
   task_manager = TaskManager(
       task_id=task_id,
       context_id=context_id,
       task_store=self._task_store,
       initial_message=None,   # <-- always None
       context=call_context,
   )
   ```

   The caller (`DefaultRequestHandlerV2._setup_active_task` / `on_message_send`) has `params.message` in hand but never passes it through.

2. `ActiveTask.start()` schedules `_run_producer()`, which calls `AgentExecutor.execute(...)`.

3. If `AgentExecutor.execute(...)` raises **before** the executor enqueues a `Task` event onto `event_queue_agent`, the `except Exception` branch in `_run_producer` (`src/a2a/server/agent_execution/active_task.py`, around lines 552-563 on `main`) runs:

   ```python
   except Exception as e:
       logger.exception('Producer[%s]: Execution failed', self._task_id)
       if request_context:
           await self._task_manager.ensure_task_id(
               self._task_id,
               request_context.context_id or '',
           )
           self._task_created.set()
       await self._event_queue_agent.enqueue_event(cast('Event', e))
   ```

4. `TaskManager.ensure_task_id` (in `src/a2a/server/tasks/task_manager.py`) finds no existing task and calls `_init_task_obj`, which constructs:

   ```python
   history = [self._initial_message] if self._initial_message else []
   return Task(
       id=task_id,
       context_id=context_id,
       status=TaskStatus(state=TaskState.TASK_STATE_SUBMITTED),
       history=history,
   )
   ```

   Because `_initial_message` is `None`, `history` is `[]`. The task is saved with `state=SUBMITTED`. The exception is then enqueued onto `event_queue_agent` — but the queue is `close(immediate=False)`'d in the `finally` and, depending on consumer ordering and which exception fired (e.g. cancellation, certain transport errors), the failed-state update may never be written. The `SUBMITTED` row stays.

The result: a persisted task row that records the existence of the task but not the message that created it, not the failure that ended it, and not even a `last_updated` timestamp (since no status event was ever processed by the consumer).

### Suggested fix

Pass the originating `Message` through to `TaskManager` so that, even if the producer fails before emitting any agent events, the persisted row at least has a populated `history`:

1. Add an `initial_message: Message | None = None` parameter to `ActiveTaskRegistry.get_or_create(...)`.
2. Forward it: `TaskManager(..., initial_message=initial_message, ...)`.
3. Update callers in `DefaultRequestHandlerV2._setup_active_task` (and the streaming variant) to pass `params.message`.

Roughly 5-10 LOC.

This alone makes the orphan row useful (you can see what the caller tried to do). A complementary improvement worth considering: in `_run_producer`'s exception branch, after `ensure_task_id`, explicitly transition the task to `TASK_STATE_FAILED` synchronously (rather than relying on the consumer to process the enqueued exception against an already-closing queue), so no row remains stuck in `SUBMITTED`.

### Reproduction sketch

A deterministic in-process reproducer:

1. Build a `DefaultRequestHandlerV2` with a real `DatabaseTaskStore` and a mock `AgentExecutor` whose `execute()` raises immediately (e.g. `raise RuntimeError("boom")`) without enqueuing any event.
2. Drive `on_message_send` with a minimal `SendMessageRequest`.
3. After the call returns / raises, query the task store directly for the task id. The row exists with `state=SUBMITTED`, `history=[]`, `metadata=None`.

In production this fires whenever the underlying executor (or anything it awaits at the very top of `execute`) raises before producing its first `Task` event — transient downstream errors, transport hiccups, and certain cancellations are the realistic triggers.

### Impact

- Per-row impact is small (one stuck `SUBMITTED` row).
- Aggregate impact in long-running deployments is steady accumulation; we've measured ~1 in 100 tasks turning into orphans across multi-day uptimes.
- Library users currently work around this with periodic janitor sweeps (delete tasks that are `SUBMITTED` + `last_updated == None` + age > N minutes), but a library-side fix would let everyone delete that workaround.

Happy to follow up with a PR if you'd like — wanted to open the issue first to confirm the suggested direction (propagate `initial_message` + explicit `FAILED` transition in the exception path) matches what maintainers would accept.

