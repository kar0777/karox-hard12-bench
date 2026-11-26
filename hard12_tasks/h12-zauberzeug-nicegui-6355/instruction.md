You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Fix connect handlers running before tab storage is created

### Description

`_on_handshake` invokes the connect handlers via `client.handle_handshake(...)` and only *then* awaits `_create_tab_storage` (`nicegui/nicegui.py:220-223`). On a tab's **first** handshake there is no `_tabs` entry yet, so a **sync** connect handler runs inline before the entry exists and `app.storage.tab` trips its own assertion. `safe_invoke` catches it, so the page still renders — the rest of that handler is skipped and the only trace is a logged ERROR. (A reconnect is fine: `copy_tab` runs earlier and populates `_tabs`.)

An **async** handler is scheduled as a task and lands after the await, so it works. Same API, same handler body, opposite outcome depending on `def` vs `async def`; nothing in the docs for `app.on_connect` / `client.on_connect` mentions it. The documented `await ui.context.client.connected()` pattern is also safe, which is probably why this has gone unnoticed.

Independent of #6310 — that one is On Air only, this is the local Socket.IO path. #6332 mirrors `_on_handshake` into `air.py`, so it inherits the same ordering.

### Example Code

```python
from nicegui import app, ui

@ui.page('/')
def index():
    ui.context.client.on_connect(lambda: app.storage.tab.__setitem__('x', 1))
    ui.label('hello')

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='x')
```

The page renders; the server log shows:

```
ERROR nicegui:app.py:187 tab storage for 3b199ba2-... should be created before accessing it
  File "nicegui/client.py", line 463, in safe_invoke
  File "nicegui/storage.py", line 177, in tab
AssertionError: tab storage for 3b199ba2-... should be created before accessing it
```

<details>
<summary><b>Four variants, one run</b></summary>

```
client.on_connect  (sync)    FAIL: tab storage for <id> should be created before accessing it
app.on_connect     (sync)    FAIL: same
client.on_connect  (async)   OK
await client.connected()     OK
```

All four measured via the `user` fixture; the sync case additionally reproduced through a real browser handshake with the `screen` fixture (the traceback above is from that run). Clean checkout of main `0e666fd9`, and byte-identical on #6332's branch, so neither introduced it.

With `redis_url` set, the two `OK` rows dodge the assertion but are not fully safe either: `_create_tab_storage` installs the dict at `storage.py:184` and only then awaits `tab.initialize()` at `:187`, so a resumed waiter can reach a not-yet-loaded dict.

</details>

### Possible fix

Create the tab storage before the handlers run. A plain swap of the two statements is not quite enough: under Redis `_create_tab_storage` yields, and `handle_handshake` also does lifecycle bookkeeping (socket registration, cancelling the delete task, connection counting) that should not be delayed behind that await. So the split is bookkeeping first, storage next, handler invocation last. Folding the shared sequence into one `Client` method — the leave-or-take from #6279, raised again in #6310 — would fix both transports at once.

### NiceGUI Version

3.16.0.post24.dev0+0e666fd9 (main)

### Python Version

3.14.2

