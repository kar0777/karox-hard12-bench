You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Using SOS on masked variables breaks

### Summary

Direct-API SOS construction is broken for both solvers that implement it (Gurobi and Xpress, after #684). Both pass linopy variable labels as if they were solver column positions; the two are only equal when no variable in the model is masked. With a single masked entry anywhere, the SOS set is built against the wrong columns — and the solvers happen to raise rather than silently mis-build, so the bug has been invisible until you try a masked SOS variable.

### Repro

```python
# dev-scripts/repro_sos_minus1_both.py
import pandas as pd
from linopy import Model


def build():
    m = Model()
    coords = pd.Index([0, 1, 2, 3], name="i")
    mask = pd.Series([True, True, False, True], index=coords)  # one slot masked
    sos_var = m.add_variables(
        lower=0, upper=1, coords=[coords], mask=mask, name="sos_var"
    )
    m.add_sos_constraints(sos_var, sos_type=1, sos_dim="i")
    m.add_objective(-sos_var.sum())
    return m


for solver in ("gurobi", "xpress"):
    print(f"\n=== {solver} ===")
    try:
        build().solve(solver_name=solver, io_api="direct")
    except Exception as e:
        print(f"  RAISED {type(e).__name__}: {e}")
```

Output (against the `xpress-direct` branch from #684, on master for Gurobi):

```
=== gurobi ===
  RAISED IndexError: index 3 is out of bounds for axis 0 with size 3

=== xpress ===
  ?404 Error: Invalid column number passed to XPRSaddsets.
  Element 2 of your array has invalid column number 3
  RAISED SolverError
```

### Root cause

In both `_build_solver_model` implementations, the SOS code passes `var.labels` values straight into the solver's `addSOS` as if they were column indices:

- **Gurobi** (`linopy/solvers.py:1530-1532`): `gm.addSOS(sos_type, x[indices].tolist(), weights)` — `x` is `gm.addMVar(M.vlabels.shape, ...)`, indexed by *position*. The code passes linopy labels as positions.
- **Xpress** (#684, `linopy/solvers.py:2168-2170`): `problem.addSOS(indices, weights, type=sos_type)` — `problem` was built via `loadproblem`, where column *position* in the solver matches position in `M.vlabels`. Same mistake.

Whenever any variable in the model is masked, `M.vlabels` becomes non-contiguous (e.g. `[0, 2, 3]` instead of `[0, 1, 2, 3]`), and linopy label ≠ solver column position. The labels that worked correctly under the no-mask happy path now over-index the solver model.

The Xpress branch additionally filters out `-1` labels (Xpress lines 2161-2167), which the Gurobi branch doesn't — that catches *one* shape of the bug (the masked entry inside the SOS variable itself) but not the broader label-vs-position mismatch caused by masks anywhere in the model.

### Fix direction

The SOS preparation is the same logic in both solvers up to the vendor call. Worth pulling it into a single shared step that:

1. drops `-1` (missing) entries from `var.labels` and the matching weights
2. resolves the remaining linopy labels to solver column positions (e.g. via `model.variables.label_index`)
3. returns `(indices, weights)` ready for the vendor `addSOS`

Each solver then keeps just its native call. Where the helper lives is open.

Needs regression coverage with a masked SOS variable in both `test_optimization.py` (end-to-end solve) and `test_sos_constraints.py` (model construction).

