You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Auto-prune timers never run in script mode (regression from #6006)

### Reproduction

Script (`leak.py`):

```python
from nicegui import app, core, ui
from nicegui.client import Client

ui.label('any module-level UI puts NiceGUI in script mode')

@app.get('/_count')
def count():
    return {
        'script_mode': core.script_mode,
        'clients': len(Client.instances),
        'routes': len(app.routes),
    }

ui.run(reload=False, port=8080)
```

Driver:

```bash
python leak.py &
sleep 4
for i in $(seq 1 1000); do curl -s -o /dev/null http://localhost:8080/; done
curl -s http://localhost:8080/_count        # → clients=1001 routes=1010
sleep 70                                    # past default client_age_threshold=60s
curl -s http://localhost:8080/_count        # → clients=1001 routes=1010 (unchanged)
```

### Expected

After `sleep 70`, `Client.prune_instances` (registered via `app.timer(10, Client.prune_instances)` in `nicegui/nicegui.py:147`) should have run several times and pruned the 1000 stale clients whose `created` is older than 60 s.

### Actual

`prune_instances` is **never called**. Clients and their routes accumulate without bound.

### Bisect

Regression introduced by **#6006** (commit `8a527282`, 2026-05-01) — *Fix duplicate `app.timer` and lifecycle handler registration in script mode*.

| Commit | Clients after 130 s grind |
|---|---|
| `8a527282^` (pre-#6006) | 1 |
| `8a527282` (current `main`) | 1001 |

<details>
<summary>Root cause</summary>

`Timer.__init__` in `nicegui/timer.py:42-45`:

```python
coroutine = self._run_once if once else self._run_in_loop
if self._skip_registration():
    return
background_tasks.create_or_defer(coroutine(), name=str(callback))
```

`Timer._skip_registration()` returns `core.is_script_mode_re_execution()`, which is `script_mode and app.is_started`.

In `nicegui/nicegui.py:_startup`:

```python
app.start()                                 # sets _state = STARTED → is_started = True
background_tasks.create(binding.refresh_loop(), …)
app.timer(10, Client.prune_instances)       # ← skipped: is_started=True AND script_mode=True
app.timer(10, Slot.prune_stacks)            # ← skipped
app.timer(10, prune_tab_storage)            # ← skipped
if app.storage.secret is not None:
    app.timer(10, prune_user_storage)       # ← skipped
```

\`app.start()\` flips \`is_started=True\` before the four internal \`app.timer(...)\` registrations. In script mode this puts the \`_skip_registration\` predicate permanently in the True branch, so the four NiceGUI-internal auto-prune timers are misclassified as per-client re-execution registrations and skipped — even though \`_startup\` runs **once** per process.

\`Slot.prune_stacks\`, \`prune_tab_storage\`, and \`prune_user_storage\` are affected the same way; this is not just a route/client leak — tab storage and slot stacks are also no longer pruned in script mode.

</details>

<details>
<summary>Why the fix in #6006 over-applies</summary>

PR #6006 correctly guards against duplicate registration when **user code at module level** does \`app.timer(...)\`: in script mode the user's script is re-executed via \`runpy.run_path\` per client connection, so module-level \`app.timer\` would otherwise stack a fresh timer each time.

But the same predicate is checked unconditionally inside \`Timer.__init__\`, which is also reached from NiceGUI's **internal** \`nicegui.py:_startup\`. Those four calls happen exactly once per process, never via the per-client re-execution path. The predicate has no way to distinguish "internal \`_startup\`-registered timer" from "user-script-registered timer".

</details>

<details>
<summary>Fix sketches (leaving the choice to maintainers)</summary>

Three plausible directions, in increasing order of intrusion:

1. **Reorder \`_startup\`** so the four internal \`app.timer(...)\` calls run **before** \`app.start()\` (while \`is_started=False\`). One-line move; \`_skip_registration\` would then return False for them. Need to verify the timers don't depend on anything \`app.start()\` produces.
2. **Internal-vs-user distinction**: add \`_internal: bool = False\` to \`Timer.__init__\` (or a class-level marker on a NiceGUI-only \`_AppTimer\` subclass) and bypass \`_skip_registration\` when set. The four internal calls in \`_startup\` pass \`_internal=True\`.
3. **Disable script-mode handling for the duration of \`_startup\`**: wrap the internal section in a \`with core.script_mode_suspended():\` context manager.

Option 1 is the smallest diff; option 2 is the most explicit.

</details>

### Environment

- NiceGUI \`main\` @ \`ba4b7c4\`
- Python 3.12.11, macOS 15.7.1 arm64
- Empirical confirmation: same code at \`8a527282^\` cleans up; at \`8a527282\` it doesn't.
