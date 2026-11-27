You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`prune_user_storage()` can delete user storage mid-request, causing sporadic HTTP 500

**TL;DR:**

`app.storage.user` intermittently raises `AssertionError` (→ HTTP 500) when the `prune_user_storage()` 10s timer tick fires *during* an in-flight request whose session has no connected WebSocket client and whose user-storage is already older than 10s.

The storage that `RequestTrackingMiddleware` created for the request is pruned out from under the handler before it reads `app.storage.user`, tripping the assert at `nicegui/storage.py:137`.

Sporadic and self-healing (the next request re-creates the storage). A deterministic MRE and the file:line mechanism are folded below. This report is intentionally **neutral on how to fix it** — facts only.

Reported by @joko-zauberzeug, who hit this while an agent auto-tested an app running on NiceGUI 3.14.0; independently reproduced on `main`.

## Example Code

```python
from nicegui import app, ui

@ui.page('/')
def index():
    ui.label(app.storage.user.get('greeting', 'hello'))

ui.run(storage_secret='secret')
```

## Description

Reading `app.storage.user` inside a page/request handler intermittently returns **HTTP 500** with:

```
AssertionError: user storage for <session-id> should be created before accessing it
```
raised at `nicegui/storage.py:137`.

- **Expected:** a request that reads `app.storage.user` succeeds — the storage `RequestTrackingMiddleware` created for the session is still present when the handler reads it.
- **Actual:** if the `prune_user_storage()` tick fires while the request is in flight — for a session with no connected WebSocket client whose user-storage is older than 10s — the storage is removed between middleware-create and handler-access, and the `assert` fires.

**Who hits it:** sessions that have no connected WebSocket client *and* whose user-storage is already >10s old — **HTTP-only clients (e.g. AI agents / scripts), revisits from a closed tab, or any long-lived session polled over HTTP**. (A genuine first visit is normally safe — its storage starts at age 0 — unless the handler itself stays in flight for >10s before reading `app.storage.user`.)

**Reproduction note:** hard to hit with `curl`, because it carries no cookie across requests — every request is a *fresh* session with age ≈ 0, which is never prunable mid-request. A cookie-persisting client (real/headless browser, or any client reusing the session cookie) that revisits after >10s idle hits it reliably.

<details>
<summary><b>Deterministic MRE — real middleware + real prune, forces the race every run</b></summary>

Drives the real path: `SessionMiddleware` + `RequestTrackingMiddleware` + the real `app.storage.user` property + the real `prune_user_storage()` coroutine the app's 10s timer runs. Determinism device: hold one request in flight, then age the session's storage past 10s and fire one prune tick — forcing the ordering `[middleware creates storage] → [prune tick] → [handler reads app.storage.user]`.

```python
import asyncio, os, tempfile
os.environ['NICEGUI_STORAGE_PATH'] = tempfile.mkdtemp()

import httpx
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

from nicegui import core
from nicegui.storage import RequestTrackingMiddleware, Storage
from nicegui.app.app import prune_user_storage

SECRET = 'just a test'
Storage.secret = SECRET
entered, release = asyncio.Event(), asyncio.Event()

async def handler(request):
    entered.set()
    await release.wait()  # hold the request in flight
    return JSONResponse({'greeting': core.app.storage.user.get('greeting', 'default')})

appl = Starlette(routes=[Route('/', handler)], middleware=[
    Middleware(SessionMiddleware, secret_key=SECRET),
    Middleware(RequestTrackingMiddleware),
])

async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=appl), base_url='http://t') as c:
        req = asyncio.ensure_future(c.get('/'))
        await entered.wait()
        sid = next(iter(core.app.storage._users))
        core.app.storage._users[sid].last_modified -= 20  # simulate >10s idle, no mutation
        await prune_user_storage()                         # the exact 10s-timer coroutine
        release.set()
        r = await req
    print(r.status_code, r.text)

asyncio.run(main())
```

**Actual output (on `main`):**
```
Traceback (most recent call last):
  ...
  File ".../nicegui/storage.py", line 137, in user
    assert session_id in self._users, f'user storage for {session_id} should be created before accessing it'
AssertionError: user storage for 0fc34cc7-209f-4d3a-97c0-7431da4d1ace should be created before accessing it
```

`_users` goes `1 → 0` while the request is in flight, then the handler's `app.storage.user` access asserts. This proves the assert fires when prune removes storage mid-request; it does **not** model any particular fix.
</details>

<details>
<summary><b>Mechanism (file:line)</b></summary>

- `nicegui/app/app.py:90` — `self.timer(10, prune_user_storage)` (10s tick).
- `nicegui/app/app.py:418-428` — `prune_user_storage()` removes any session **not in `Client.instances`** (no connected WS client) whose storage age `> 10.0`. It does not consider whether an HTTP request for that session is currently in flight.
- `nicegui/storage.py:37-38` — `RequestTrackingMiddleware` creates the user storage per request if missing.
- `nicegui/storage.py:137` — the `user` property `assert`s the storage exists.
- `nicegui/observables.py:24,35-36` — `last_modified` is set on creation and bumped via `_handle_change()` on mutation; a **read never bumps it**, so a session that is only read ages out after 10s.

This surfaced as a regression when `app.storage.user` changed from lazy-create to `assert` in #4074 (before that commit, a missing user storage was silently re-created on access). This issue takes **no position on the fix**.
</details>

<details>
<summary><b>User-side mitigation (not a proposed framework fix)</b></summary>

Affected apps can wrap `app.storage.user` reads in `try/except` with a fallback default. Noted for others who hit this in the wild — not a suggestion for how NiceGUI should resolve it.
</details>

## NiceGUI Version

Reported on `3.14.0`; independently reproduced on `main`. The relevant code is identical across both.

## Python Version

`3.12` (not Python-version-specific).

## Browser

Chrome (headless) — also reproducible with **no browser** (plain HTTP client reusing the session cookie).

## Operating System

macOS (OS-independent).

## First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue.
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI.
- [x] I used the GitHub search to find a similar issue and came up empty (the only nearby match, #5077, is a different assert from the same 10s timer).

