You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[PERF] Build pivot_longer reorder indexer with one NumPy allocation

## Summary

`_build_indexer_reorder_contents` currently constructs `np.arange(length * reps)`, reshapes it, and ravels in Fortran order. Because the final ravel requires a reordered copy, the helper temporarily holds roughly twice the output allocation.

A mathematically equivalent NumPy formulation can construct the row-by-column offsets directly:

```python
rows = np.arange(length)[:, None]
columns = np.arange(reps) * length
indexer = np.add(rows, columns).ravel()
```

This keeps the implementation in NumPy, preserves the current positional contract, and substantially lowers peak temporary memory.

## Measurements

Same-process medians on pandas 3.0.5 / NumPy 2.3.5:

| Shape | Current | One-allocation formulation | Current peak | New peak |
| --- | ---: | ---: | ---: | ---: |
| `length=100_000`, `reps=20` (2M output) | 1.49 ms | 1.49 ms | 30.52 MiB | 16.15 MiB |
| `length=1_000`, `reps=1_000` (1M output) | 1.09 ms | 0.63 ms | 15.26 MiB | 7.77 MiB |
| `length=1_000_000`, `reps=8` (8M output) | 10.53 ms | 8.11 ms | 122.07 MiB | 68.79 MiB |

The generated arrays were element-for-element equivalent.

## Scope

- Replace only `_build_indexer_reorder_contents`.
- Add focused helper equivalence tests for zero/small sizes and both row-heavy and column-heavy shapes.
- Confirm public `pivot_longer` behavior for extension arrays with `sort_by_appearance=True`.
- Measure end-to-end runtime and peak memory on many-row and many-column workloads.
- Preserve `np.intp`-compatible indexing and overflow/error behavior.

## Acceptance criteria

- Exact positional equivalence with the current helper.
- No ordering or dtype regression across nullable integer, string, categorical, datetime, and timezone-aware extension arrays.
- Peak helper allocation materially decreases for large outputs.
- No meaningful runtime regression for small or representative workloads.
- Complete pivot tests pass under supported pandas environments.

## Dependencies

Land after #1636 / PR #1643 so its allocation changes remain independently reviewable. This NumPy baseline should precede any Rust experiment in pyjanitor-devs/janitor-rs#18.
