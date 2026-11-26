You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

clear_out_obsolete_test_names never persists its cleanup: counters iterate keys instead of values

`ListAllTestsResult.clear_out_obsolete_test_names` (`src/mutmut/__main__.py`, lines 421–433 on `main`) filters obsolete test names out of `tests_by_mangled_function_name` correctly, but the guard around `save_stats()` can never be true, so the cleaned state is never written back to `mutants/mutmut-stats.json`.

```python
count_before = sum(len(x) for x in mutmut.tests_by_mangled_function_name)   # line 422
...
count_after  = sum(len(x) for x in mutmut.tests_by_mangled_function_name)   # line 430
if count_before != count_after:
    print(f"Removed {count_before - count_after} obsolete test names")
    save_stats()
```

`tests_by_mangled_function_name` is a `defaultdict(set)` (`src/mutmut/__init__.py`, line 15). Iterating it yields **keys**, so `len(x)` measures the length of each mangled function name, not the size of its test set. The dict comprehension in between preserves every key, so both sums are computed over an identical key set and `count_before == count_after` **always** — not intermittently. The branch is dead: the message never prints and `save_stats()` never runs from here.

### Impact

Limited but persistent. The in-memory filtering happens before `tests_for_mutant_names` is used, so runs are unaffected and no verdict is wrong. What lingers is the file on disk: obsolete node IDs stay in `mutmut-stats.json` indefinitely, unless something else happens to call `save_stats()` in the same process (for example `run_stats_collection` when new tests are found). Anyone reading the stats file therefore sees a state no run has ever used.

### Reproduce

1. Run `mutmut run` on a project until stats are cached.
2. Delete or move one test file.
3. Run `mutmut run` again.
4. `mutants/mutmut-stats.json` still contains that file's node IDs under `duration_by_test` and `tests_by_mangled_function_name`, and `Removed N obsolete test names` is never printed.

### Suggested fix

```python
count_before = sum(len(x) for x in mutmut.tests_by_mangled_function_name.values())
count_after  = sum(len(x) for x in mutmut.tests_by_mangled_function_name.values())
```

in both places, which also makes the reported number mean what the message says.

Observed on 3.7.0; the code is unchanged on `main`. Happy to send a PR if that is easier than fixing it directly.

