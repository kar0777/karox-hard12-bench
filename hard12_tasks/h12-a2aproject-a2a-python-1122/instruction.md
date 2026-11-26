You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ActiveTask producer task GC'd while pending — 'Task was destroyed but it is pending!' at turn boundaries

### Version
`a2a-sdk` 1.1.0 (the same code is present on `main` today: `src/a2a/server/agent_execution/active_task.py`).

### Symptom
Under continuous load, `asyncio` logs a recurring error:

```
ERROR asyncio Task was destroyed but it is pending!
task: <Task pending name='producer:<uuid>' coro=<ActiveTask._run_producer() running at
      a2a/server/agent_execution/active_task.py:566>
```

Every occurrence is a `producer:<uuid>` task at the same coroutine, firing every ~1–4 min under load and clustering at request/turn completions (observed 103× over a multi-hour run of an always-on server using `DefaultRequestHandler`).

### Analysis
`ActiveTask._producer_task` is created in `start()` and is only ever explicitly `cancel()`ed on the **cancel path** — `cancel()` does `self._producer_task.cancel()` and the flow awaits completion (`active_task.py` ~L703–723).

On the **normal-completion teardown path** it isn't. `_run_consumer`'s `finally` sets `_is_finished`, shuts down `_request_queue`, and calls `_maybe_cleanup()`, which calls `self._on_cleanup(self)` — releasing the `ActiveTask` **without cancelling or awaiting `_producer_task`**. Between turns the producer is parked pending on `await self._request_queue.get()`; when the last strong reference to the `ActiveTask` (which owns `_producer_task`) is dropped, the still-pending producer is garbage-collected → the asyncio warning. The producer that was mid-shutdown is abandoned rather than flushed/cancelled deterministically.

So the two teardown paths are asymmetric: `cancel()` tears the producer down cleanly; normal completion leaks it.

### Impact
Mostly log noise, but a producer torn down without a clean `cancel()` + `await` is a latent correctness risk — anything it was mid-way producing (or its `finally` cleanup, which closes the event queues) isn't guaranteed to run deterministically.

### Suggested fix
On the normal cleanup path, cancel `_producer_task` and `await` it (suppressing `CancelledError`) before `_on_cleanup(self)` — or `await asyncio.gather(self._producer_task, self._consumer_task, return_exceptions=True)` at teardown — mirroring what `cancel()` already does.

Happy to provide a minimal reproducer if that would help.
