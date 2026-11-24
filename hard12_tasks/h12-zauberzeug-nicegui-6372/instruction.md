You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

@await_on_shutdown has no effect for handlers invoked in a client context (on_connect, on_click, ui.timer)

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue.
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar issue and came up empty.

### Example Code

```python
import asyncio
from pathlib import Path

from nicegui import app, background_tasks, ui

OUT = Path('shutdown_probe.txt')
OUT.unlink(missing_ok=True)


@background_tasks.await_on_shutdown
async def save(tag: str) -> None:
    await asyncio.sleep(3)  # still in flight when the shutdown below fires
    with OUT.open('a') as f:
        f.write(tag + '\n')


async def stop_soon() -> None:
    await asyncio.sleep(2)
    app.shutdown()


app.on_startup(lambda: save('on_startup'))  # works
app.on_connect(lambda: save('on_connect'))  # broken
app.on_startup(stop_soon)

ui.label('open this page once, then wait a few seconds')
ui.run(reload=False)
```

### Description

`@background_tasks.await_on_shutdown` is documented as *"Tag an async function so tasks created from it won't be cancelled during shutdown."* That holds for `app.on_startup`, but **not** for handlers invoked in a client context — they are cancelled at shutdown anyway, silently.

Run the snippet above, let the page load once, and wait for the automatic shutdown. `shutdown_probe.txt` should contain both lines. Actual output:

```
on_startup
```

`on_connect` is missing. Both went through the same decorator; only the one that did not pass through a client context survived. `on_startup` here is the control — it proves shutdown really does await protected work, so the difference is not the grace period.

I measured three affected entry points, all still cancelled:

| entry point | dispatch path |
|---|---|
| `app.on_connect(handler)` / `client.on_connect(...)` | `Client.safe_invoke` |
| `ui.button(on_click=handler)` | `handle_event` |
| `ui.timer(0.01, handler, once=True)` | `Timer` |

### Mechanism

`background_tasks.create()` recognises protected work by identity:

https://github.com/zauberzeug/nicegui/blob/main/nicegui/background_tasks.py#L47

Every context-preserving dispatch path wraps the awaitable in a **fresh coroutine** before calling `create()`, so that `isinstance` check no longer matches:

- `nicegui/client.py:455` and `:482` — `helpers.await_with_context(result, ...)`
- `nicegui/events.py:486` — `_await_and_handle_in_context(result, parent_slot)`
- `nicegui/timer.py:45` — `coroutine()`

`App.safe_invoke` (`nicegui/app/app.py:110`) passes `result` straight through, which is why `on_startup` is the one that works.

This is **not a regression** — I checked, expecting one. `#5879` replaced a hand-rolled `async def result_with_client()` wrapper in `safe_invoke` with the shared `await_with_context` helper, but the old code wrapped the awaitable too, so the marker was already being hidden. The behaviour dates back to `@await_on_shutdown` and `safe_invoke` first coexisting, and reproduces on `v3.16.0`.

Worth noting the documented example works, which is probably why this has gone unnoticed — [`section_configuration_deployment.py:186`](https://github.com/zauberzeug/nicegui/blob/main/website/documentation/content/section_configuration_deployment.py#L186) uses `on_click=lambda: background_tasks.create(backup())`, and that extra `lambda` hands `create()` the marker directly. Only the shorthand `on_click=backup` fails.

I have not proposed a fix — whether the marker should be propagated through the wrappers, detected differently, or the docstring narrowed to match feels like your call.

### NiceGUI Version

3.16.0 (also reproduced on `main`)

### Python Version

3.14.0

### Browser

Chrome

### Operating System

macOS

### Additional Context

Found while reviewing #6329, which fixes the same *class* of marker loss one layer down (a requeued lazy task losing its protection). That PR's fix does not cover these paths — I re-measured all three against its branch and they are still cancelled.
