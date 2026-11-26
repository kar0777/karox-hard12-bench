You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

groupby().sum() returns wrong dims for a multi-dimensional DataArray grouper (fast path)

Likely a regression from #802 

> [!Note]
> created by AI

### Bug

`Variable.groupby(...).sum()` returns wrong dimensions when grouping by a **multi-dimensional** `DataArray` grouper on its default (fast) path. The reduction happens over only one of the grouper's dimensions, and the other survives in the result — producing incorrect (and silently wrong) grouped constraints/expressions.

The `use_fallback=True` escape hatch (native xarray groupby) gives the correct result.

### Root cause

In `LinearExpressionGroupby.sum` (`linopy/expressions.py`), the fast path does `group = group.to_pandas()` for a `DataArray` grouper. For a 2-D grouper this yields a `DataFrame`, which is then routed through the *multikey* encoding path — reducing over only the row axis and leaving the column axis in the output. A genuinely N-D grouper (whose values should define the groups over all its dims jointly) is not handled.

### Minimal reproducer

```python
import linopy, xarray as xr

# 2x2 grid, grouped into 2 groups by a 2-D grouper; extra dim 'k' should be preserved
grp = xr.DataArray([[1, 1], [2, 2]], dims=["i", "j"],
                   coords={"i": [0, 1], "j": [0, 1]}).rename("g")

m = linopy.Model()
v = m.add_variables(coords=[[0, 1], [0, 1], [0, 1]], dims=["i", "j", "k"], name="v")

print(v.groupby(grp).sum().dims)                    # ('j', 'k', 'g', '_term')  <- stray 'j', WRONG
print(v.groupby(grp).sum(use_fallback=True).dims)   # ('g', 'k', '_term')        <- correct
```

Plain xarray reduces the same 2-D grouper correctly over both dims, so the expected result is `('g', 'k', '_term')` (group dim + the untouched `k`).

### Impact

Silent incorrectness: expressions/constraints built via `groupby().sum()` with a multi-dim grouper are wrong unless the user knows to pass `use_fallback=True`. Surfaced while writing the `examples/sudoku.ipynb` example (grouping a `(row, column, digit)` variable by a 2-D `(row, column)` square-index grouper), which currently has to carry `use_fallback=True` as a workaround.

### Environment

- linopy `0.8.0.post1.dev109+ge87efc1f4`
- xarray `2026.4.0`

### Suggested fix

Detect a multi-dimensional `DataArray` grouper on the fast path and either handle it directly or route it to the native-xarray (fallback) implementation instead of `to_pandas()`-ing it into a multikey `DataFrame`.

