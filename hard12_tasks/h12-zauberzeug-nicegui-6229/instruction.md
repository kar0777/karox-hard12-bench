You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Repeating ui.timer raises "The parent slot of Timer(id=N) has been deleted" when its client is deleted while waiting in _can_start() — the _should_stop() guard is unreachable

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
from nicegui import ui


@ui.page('/')
def page() -> None:
    ui.timer(60, lambda: None)


ui.run()
```

Then request the page over plain HTTP without ever opening the websocket (a bot, a prefetch, a user bouncing before the handshake, an HTTP-only load probe):

```bash
curl -s http://localhost:8080/ > /dev/null
```

After `Client.prune_instances` deletes the never-connected client (~60 s), the timer task wakes and — depending on a garbage-collection race — dies with:

```
  File "nicegui/background_tasks.py", line 152, in _handle_exceptions
    task.result()
  File "nicegui/timer.py", line 90, in _run_in_loop
    with self._get_context():
  File "nicegui/elements/timer.py", line 15, in _get_context
    return self.parent_slot or nullcontext()
  File "nicegui/element.py", line 150, in parent_slot
    raise RuntimeError(f'The parent slot of {name}(id={self.id}{markers}) has been deleted.')
RuntimeError: The parent slot of Timer(id=2) has been deleted.
```

Because it races the cycle collector it is intermittent per occurrence — but at fleet scale it is loud: on our staging deployment this single raise is **~49% of all captured Sentry events** (~3,400 events across two message wordings, 3.14.x: "The parent slot of the element has been deleted.").

### Description

The sequence:

1. A repeating `ui.timer` is created during page build. `_run_in_loop` suspends in `_can_start()` on `await self.client.connected()` while the websocket handshake is pending.
2. The client never connects and is deleted (`prune_instances`, or any other `Client.delete()` while the timer still waits).
3. `Client.delete()` runs `remove_all_elements()` (which cancels the timer via `_handle_delete`) and then `self._connected.set()  # for terminating connected() waits` — which wakes the parked waiter into a **success** return. `_can_start()` answers `True` for a deleted client.
4. `_run_in_loop` proceeds to `with self._get_context():`. If the cycle collector has already collected the slot tree, the `parent_slot` weakref dereferences to `None` and `element.py` raises — **one line before** `while not self._should_stop():`, the guard built for exactly this case (`self.is_deleted` is already `True` at this point and would exit cleanly).

So the timer is already properly canceled and deleted; it just touches the dead slot before it is allowed to notice. No application frame appears in the stack, and no user ever sees anything — but every occurrence goes through `app.handle_exception` at ERROR level, which is costly for anyone forwarding logs to a paid error tracker.

**Suggested fix:** check `self._should_stop()` before entering `self._get_context()` in `_run_in_loop` (and equivalently `self.active and not self._should_stop()` before the context in `_run_once`). At the failure point `_deleted` is `True`, so the hoisted check exits cleanly, and `Timer._cleanup` is already guarded by `if not self._deleted:` so the finally-path stays safe.

A complementary (or alternative) fix would be for `_can_start()` to return `False` when the wake came from `Client.delete()` rather than a real connection — e.g. re-checking `self.client.id in Client.instances` / `self.is_deleted` after `connected()` returns — since `connected()` currently reports success on a deleted client.

### NiceGUI Version

3.15.0 (same raise with the older message wording on 3.14.x)

### Python Version

3.14.6

### Browser

Not applicable (server-side; triggered by HTTP-only page loads)

### Operating System

Linux (Docker)

### Additional Context

The two suspension points and the GC dependency make this hard to reproduce deterministically in a unit test — the raise only happens when the cycle collector runs between the `connected()` wake-up and the timer task's resumption — but the code path above is fully deterministic once the weakref is dead.

