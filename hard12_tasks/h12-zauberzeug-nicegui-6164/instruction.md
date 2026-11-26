You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

ObservableDict.pop() (and app.storage.*) returns None for a missing key instead of raising KeyError

*Filed by Claude Code on @evnchn's behalf.*

### Example Code

```python
from nicegui import app

# app.storage.general (and .user / .tab / .client) is an ObservableDict,
# so this is reachable straight from the public storage API:
print(repr(app.storage.general.pop('nonexistent')))   # prints: None
#                                                        a plain dict raises KeyError here

# minimal, no server needed:
from nicegui.observables import ObservableDict
d = {}
try:
    d.pop('missing')
except KeyError:
    print("plain dict  -> KeyError   (correct)")
print("ObservableDict ->", repr(ObservableDict().pop('missing')))   # -> None   (wrong)
```

### Description

`ObservableDict.pop()` breaks the `dict.pop()` contract: **popping a missing key with no default returns `None` instead of raising `KeyError`.**

The signature is `pop(self, k, d=None)`, so `super().pop(k, d)` is *always* called with a default — the method can never tell "no default given" from "explicit default of `None`", and therefore never raises. [Python's `dict.pop`](https://docs.python.org/3/library/stdtypes.html#dict.pop) is: missing key **with** default → return default; missing key **without** default → raise `KeyError`.

This is user-facing, not just internal: `app.storage.general`, `app.storage.user`, `app.storage.tab`, and `app.storage.client` are all `ObservableDict`s (via `PersistentDict(ObservableDict, ...)`), so `app.storage.user.pop('key_that_might_be_absent')` silently returns `None` where a normal dict would raise — a foot-gun for code that relies on the exception to distinguish "absent" from "present but `None`".

Expected: `app.storage.general.pop('nonexistent')` raises `KeyError`.
Actual: it returns `None`.

**Secondary symptom (same root cause):** `pop()` fires a change event even when nothing was removed. A no-op call still bumps `last_modified`, notifies observers, and can schedule a persistent-storage write / UI update:

```python
from nicegui.observables import ObservableDict
fired = []
d = ObservableDict(on_change=lambda: fired.append(1))
d.pop('missing', 'default')     # returns 'default', mutates nothing...
print(fired)                    # -> [1]   (a spurious change event)
```

Expected: `pop(k, default)` on a missing key mutates nothing → fires no change event.
Actual: one change event fires.

Note: this is **pre-existing** (not introduced by the recent observables rework in #6140 — confirmed reproducing identically on `main` and on that branch); surfaced while reviewing it. A fix PR will follow.

### NiceGUI Version

3.14.0 (also reproduces on `main` @ `8c51e15b`)

### Python Version

3.13.11

### Browser

Other — not browser-related; this is server-side Python behavior of `ObservableDict` / `app.storage`.

### Operating System

macOS (platform-independent — pure-Python logic in `nicegui/observables.py`)

### Additional Context

Root location: [`nicegui/observables.py`](https://github.com/zauberzeug/nicegui/blob/main/nicegui/observables.py) — `ObservableDict.pop`. `ObservableList.pop` / `ObservableSet.pop` have different signatures and are unaffected. Internal callers that want tolerant removal already pass an explicit default (e.g. `props.py`), so raising `KeyError` for the no-default case aligns with `dict` without breaking them.

