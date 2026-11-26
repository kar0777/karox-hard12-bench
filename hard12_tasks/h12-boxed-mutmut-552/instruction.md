You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Trampoline misses mutants when tests use `patch.dict(os.environ, ..., clear=True)`

## Description

When a test uses `unittest.mock.patch.dict(os.environ, {...}, clear=True)`, the
generated trampoline reads `MUTANT_UNDER_TEST` from `os.environ`, finds it
empty, and forwards the call to the **original** function. Mutants reachable
only through such tests are then falsely reported as `survived`. This silently
lowers the mutation score of any project whose tests scrub the environment
(Docker / runtime detection, default-paths logic, env-driven feature flags,
etc.).

## Root Cause

`_mutmut_trampoline` re-reads `MUTANT_UNDER_TEST` on every call:

[`mutation/trampoline_templates.py` L121-L125](https://github.com/boxed/mutmut/blob/main/mutmut/mutation/trampoline_templates.py#L121-L125)

```python
def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ.get('MUTANT_UNDER_TEST', '')
    if not mutant_under_test:
        # No mutant being tested - call original function
        ...
```

mutmut sets `MUTANT_UNDER_TEST` once in the forked child
([`__main__.py` L1052-L1055](https://github.com/boxed/mutmut/blob/main/mutmut/__main__.py#L1052-L1055))
before importing the test target, and the value never legitimately changes
during that child's lifetime. The per-call `os.environ.get(...)` therefore
serves no functional purpose given that lifecycle, but exposes the trampoline
to test code that scrubs `os.environ`.

## Reproducer

```python
# orchard/runtime.py
def is_in_docker() -> bool:
    return os.environ.get("IN_DOCKER", "0") == "1"

# tests/test_runtime.py
def test_is_in_docker():
    with patch.dict(os.environ, {"IN_DOCKER": "1"}, clear=True):
        assert is_in_docker()
```

If this is the only test exercising `is_in_docker`, **all** of its mutants
(`"0" → "1"`, `== → !=`, etc.) survive, even though the assertion would
catch them in a normal run.

## Current Workaround

Projects work around this with a per-test helper that re-injects
`MUTANT_UNDER_TEST` into the patched env:

```python
def mutmut_safe_env(**extra: str) -> dict[str, str]:
    env: dict[str, str] = {}
    mut = os.environ.get("MUTANT_UNDER_TEST")
    if mut is not None:
        env["MUTANT_UNDER_TEST"] = mut
    env.update(extra)
    return env

# in tests:
with patch.dict(os.environ, mutmut_safe_env(IN_DOCKER="1"), clear=True):
    ...
```

It works, but bleeds mutmut implementation details into every test that
needs `clear=True`.

## Proposed Fix: two options

### Option A: sticky cache on the trampoline (slightly recommended)

Remember the last non-empty value seen, so a wiped env falls back to it:

```python
def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ.get('MUTANT_UNDER_TEST', '')
    if not mutant_under_test:
        mutant_under_test = getattr(_mutmut_trampoline, '_sticky', '')
    else:
        _mutmut_trampoline._sticky = mutant_under_test
    if not mutant_under_test:
        # No mutant being tested - call original function
        ...
```

A few added lines: one conditional that updates the sticky cache on non-empty
env and falls back to it on empty env. Each non-empty transition refreshes the
cache, so the parent's transitions through `"fail"`, `"stats"`,
`"list_all_tests"`, `"mutant_generation"`, and per-mutant names all keep
working.

**Behavioral difference vs. current code.** The parent process today
intentionally writes `MUTANT_UNDER_TEST=""` between phases (after
`run_forced_fail_test` at [`__main__.py:640`](https://github.com/boxed/mutmut/blob/main/mutmut/__main__.py#L640)
and after `mutant_generation` at [`__main__.py:994`](https://github.com/boxed/mutmut/blob/main/mutmut/__main__.py#L994))
as a "transition signal" between phases. With Option A, the sticky cache
ignores those resets and keeps reporting the previous mode. This is only
observable if the parent invokes user code through a trampoline *between* such
a reset and the start of the next phase. It does not affect the per-mutant
test runs themselves: those happen in `os.fork()`ed children whose env is set
once at fork time and never cleared, so live read and sticky cache are
equivalent there.

### Option B: import-time cache + live fallback

Snapshot once at module-import time:

```python
_MUTANT_UNDER_TEST_CACHED = os.environ.get('MUTANT_UNDER_TEST', '')

def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg=None):
    """Forward call to original or mutated function, depending on the environment"""
    mutant_under_test = (
        _MUTANT_UNDER_TEST_CACHED
        or os.environ.get('MUTANT_UNDER_TEST', '')
    )
    if not mutant_under_test:
        ...
```

Faster than Option A (skips the per-call `os.environ.get` once the cache is
populated, measurable on suites with tens of thousands of trampoline
crossings). Relies on the trampoline impl being imported *after*
`MUTANT_UNDER_TEST` is set, which is true today but is a stricter assumption
than Option A.

## Verified in a real codebase

Reproduced and fixed in [orchard-ml](https://github.com/tomrussobuilds/orchard-ml)
on `orchard/core/environment/hardware.py`, where every test for
`configure_system_libraries` uses `patch.dict(os.environ, ..., clear=True)`:

| Setup | Killed | Survived | Score |
|---|---|---|---|
| `mutmut_safe_env` workaround active | 129 / 133 | 4 | **97.0 %** |
| Workaround disabled, trampoline unchanged | 114 / 133 | 19 | **85.7 %** |
| Workaround disabled, **Option A patched** | 129 / 133 | 4 | **97.0 %** |

15 mutants were falsely surviving without the workaround. Option A restores
the score exactly without it.

## Recommendation

Both options have tradeoffs.

**Option A** is minimal and works correctly in the fork-and-test path. Its
risk is parent-side: if user code is invoked through a trampoline between an
`""` reset and the next phase, the sticky cache would still report the
previous mode. I have not been able to find a code path in mutmut that
actually triggers this today, but the assumption is worth pointing out.

**Option B** is faster but has a sharper edge case: if the parent imports
`trampoline_impl` while `MUTANT_UNDER_TEST` is set to a non-mutant value
(`"stats"`, `"fail"`, etc.), the import-time cache freezes that value, and
forked children inherit it via copy-on-write. Their per-mutant env would then
be ignored. Option B is therefore only safe if `trampoline_impl` is
guaranteed to be imported after fork and after the env is set, which is not
the case today.

On balance I'd lean toward **Option A**, but I'm happy to implement either
(or a different approach you prefer).

