You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: append=True with unknown artifact_id silently drops the chunk — should fail loudly

### What happened?

When `TaskUpdater.add_artifact(append=True, ...)` is called with an `artifact_id` that doesn't exist on the task yet, the chunk is silently dropped after a `logger.warning`. This is a footgun — the wire delivers a successful response while the streamed content is lost.

#### Reproducer (concept)

```python
from uuid import uuid4
from a2a.types.a2a_pb2 import Part

# Inside an AgentExecutor.execute(...):
async for chunk in some_async_source():
    await updater.add_artifact(
        # No artifact_id — TaskUpdater auto-generates a fresh one on
        # EVERY call. Each call hits the warning path because the
        # newly-generated id has no prior artifact to append to.
        parts=[Part(text=chunk)],
        name="my_response",
        append=True,
        last_chunk=False,
    )
```

Each `add_artifact` call produces:

```
WARNING  a2a.server.tasks.task_manager:task_manager.py:79 Received append=True for nonexistent artifact index <fresh-uuid> in task <task-id>. Ignoring chunk.
```

…and the chunk is dropped. The Task transitions through WORKING → COMPLETED with an empty artifact, no error surfaces upward, and the client sees a successful response with no content.

The fix is to pin `artifact_id = uuid4().hex` once per turn and pass it on every `add_artifact` call — but you only learn this from reading the SDK source or finding a worked example. The first time we hit this, the only signal was a downstream test that asserted on artifact text; if the test had only asserted HTTP status we'd have shipped the regression.

#### Suggested fix

Surface the failure path loudly. Two options, ranked by invasiveness:

1. **Raise instead of warn** in [`task_manager.py:append_artifact_to_task`](https://github.com/a2aproject/a2a-python/blob/main/src/a2a/server/tasks/task_manager.py#L79). A `ValueError` (or a dedicated subclass) makes the misuse impossible to miss. Existing well-formed callers see no change; misusers see a clear stack trace pointing at their `add_artifact` call instead of a silently-empty response.

2. **Or**: have `TaskUpdater.add_artifact` itself remember the most-recently-allocated id when `artifact_id is None`, so a sequence of `add_artifact(append=True, ...)` calls without explicit ids implicitly target the same artifact. This changes default behaviour but matches the natural mental model of "I'm streaming chunks of one thing."

Option 1 is the minimal/safest change. Option 2 is more ergonomic but is a behaviour change, so might want a deprecation cycle.

#### Why it matters

Streaming `artifact_update` events is the main reason a server sets `capabilities.streaming=True`. The current SDK behaviour means the streaming path is a footgun for any server-side executor that doesn't already know the `artifact_id`-pinning trick. Loud failure beats silent drop.

Happy to send a PR for option 1 if maintainers agree on the approach.

#### Environment

- a2a-sdk 1.0.2
- Python 3.12.4

### Relevant log output

```shell
WARNING  a2a.server.tasks.task_manager:task_manager.py:79 Received append=True for nonexistent artifact index 20ba23dd-68e8-4f62-9ff0-42f9c9fa79e4 in task 87481320-93bd-456d-add0-2ccc6fe8e48b. Ignoring chunk.
WARNING  a2a.server.tasks.task_manager:task_manager.py:79 Received append=True for nonexistent artifact index c4569d04-6a52-493a-931d-a70725368721 in task 87481320-93bd-456d-add0-2ccc6fe8e48b. Ignoring chunk.
```
