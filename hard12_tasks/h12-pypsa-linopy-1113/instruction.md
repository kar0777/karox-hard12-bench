You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

WindowModel.solve: option to disable warm start across windows (in-place update is 2.7x slower)

> [!NOTE]
> This issue was drafted with AI assistance (Claude) and reviewed by the author.

## Describe the feature you'd like to see

An option to solve each window of a `WindowModel` without the warm start from the previous window, e.g. `w.solve(..., warm_start=False)`.

`WindowModel.solve` keeps one native solver model and updates it in place for each `advance` (`Solver.solve_window`). HiGHS then starts simplex from the previous window's basis. In a rolling horizon the windows are shifted in time, so that basis is a poor start and the solve gets much slower.

Benchmark: PyPSA `scigrid_de` tiled to 192 hourly snapshots (585 buses, storage units, ramp limits), full model built once, 4 windows of 48 snapshots via `restrict`/`advance` with `fix` for all out-of-window values, HiGHS simplex:

| mode | solve time, 4 windows | sum of window objectives |
|---|---|---|
| in-place update (current) | 201.5 s | 54420133.960307 |
| fresh solver per window (`w._solver = None`) | 74.5 s | 54420133.960305 |

The same effect appears with `Solver(..., track_updates=True)` reused across separately built window models.

Sketch of the loop used:

```python
m = n.optimize.create_model()  # full horizon
w = None
for sns in windows:
    w = m.restrict(snapshot=sns, fix=full) if w is None else w.advance(snapshot=sns, fix=full)
    w._solver = None  # workaround: drop warm start
    w.solve("highs", output_flag=False)
```

Implementation ideas: a `warm_start: bool` (or `reuse: bool`) argument on `WindowModel.solve`, which either rebuilds the native model, or keeps the in-place update but clears the basis/solution before solving (e.g. `Highs.clearSolver()` for HiGHS). The second option keeps the cheap update and avoids the bad start. The default for rolling-horizon use should probably be no warm start.

Related: #768, #1109, #1110.

