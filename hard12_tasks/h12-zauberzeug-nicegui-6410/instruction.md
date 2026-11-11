You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Per-client memory: ~14% saving from `__slots__` on the observable collections


On the measured ~178-element page, each connected client used about **1.2 MB of traced Python memory**. About a quarter of that is the per-element `Props`/`Classes`/`Style` collections. Adding `__slots__` to `ObservableDict`/`ObservableList`/`ObservableSet` and `Props`/`Classes`/`Style` cuts per-client memory by **~14%** (1231 → 1059 KiB) with a 7-line change. The relevant tests pass.

The trade-off: direct instances of those classes lose `vars()` and arbitrary attributes. Subclasses without their own `__slots__` (e.g. `PersistentDict`) regain a `__dict__`; the subclass cases I tested passed.

Would a PR for this be welcome, or is the compatibility cost not worth it?

<details><summary>Measurements</summary>

Setup:
- `4.0` branch @ 7639f86ab, Python 3.13, macOS.
- A ~178-element page: 10 bound labels, a 1 s timer, 40 cards with label/button/input, a 20-row table.
- 50 real Chromium clients via Playwright.
- `tracemalloc` started before the import; snapshots after `gc.collect()` at 0, 1 and 50 clients.
- Per client = (50 − 0) / 50, which agrees with (50 − 1) / 49 to within 1 KiB.

Four interleaved runs (ABAB), fresh process each, median [range]:

| | KiB per client | change |
|---|---|---|
| `4.0` | 1231.0 [1230.7, 1232.0] | — |
| `__slots__` patch | 1058.7 [1057.4, 1060.2] | −172 (−14%) |
| `4.0` with `ws_per_message_deflate=False` | 929.1 [928.3, 930.3] | −302 (−24.5%) |

The ranges don't overlap. These are traced Python allocations, not RSS.

Top allocation sites, KiB per client:
- wsproto zlib compressor: 262; inflater: 32.
- `observables.py:37` (instance `__dict__`): 206.
- `binding.py:286` (`bindable_properties` key): 68, plus weakref entries: ~44.
- `observables.py:27` (`_change_handlers`): 65.
- `observables.py:28` (`_observer_refs`): 33.

</details>

<details><summary>What else showed up (not part of the proposal)</summary>

- **WebSocket compression** is about 24% per client. `ws_per_message_deflate` is already passed through `ui.run`, so this is a documented memory-vs-bandwidth trade, not a default to change.
- **The `bindable_properties` registry:** every `BindableProperty.__set__` writes an entry even when nothing is bound (e.g. `visibility.py:16` for every element). A ~20-line prototype that registers each object once instead of each (object, name) pair saves a further ~106 KiB per client (−8.6%, non-overlapping ranges), and binding verdicts matched the current registry on all 268 binds in the binding tests. It is not strictly behaviour-identical in a few contrived cases (e.g. classes hiding attributes from `dir()`), so it would need its own discussion; not part of this proposal.
- **Ruled out:** the outbox history is bounded and pruned on ack; I found no per-client copies of static data.

</details>

<details><summary>Patch and tests</summary>

A 7-line change in `observables.py` and `props.py`/`classes.py`/`style.py`. `ObservableSet` already supports weakrefs, so only dict and list get a `__weakref__` slot.

Passing tests: `test_observables`, `test_binding`, `test_element`, `test_element_delete`, `test_storage`, `test_table`, `test_user_simulation`, `test_select` (295 passed). ruff is clean.

Copy, pickle, weakref, subclass and `FilePersistentDict` smoke checks pass.

</details>

