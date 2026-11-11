You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Solve log reports the objective in scaled (solver) units when objective scaling is set

> This issue was drafted with AI assistance.

### Version Checks

- [x] I have confirmed this bug exists on the latest release (v0.10.1) of Linopy.
- [x] I have confirmed this bug exists on the current `master` branch of Linopy (9ad435d3, by source inspection).

### Issue Description

With `m.add_objective(..., scaling=s)`, the " Optimization successful" log message prints the raw solver objective (`objective * s`), while `m.objective.value` is correctly divided back. The log is the first place users look, so with e.g. `scaling=1e-3` it is off by a factor 1000 without any hint.

`Model.assign_result` logs the `Result` *before* unscaling:

- `linopy/model.py` (`assign_result`): `result.info()` is called, then `self.objective._value = result.solution.objective / self.objective.scaling`
- `linopy/constants.py` (`Result.__repr__`): `f"Objective: {self.solution.objective:.2e}\n"`

`Result.solution.objective` (and `report.dual_bound`) stay in solver units, so the log shows those values.

### Reproducible Example

```python
import logging

from linopy import Model

logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")

m = Model()
x = m.add_variables(lower=0, name="x")
y = m.add_variables(lower=0, name="y")
m.add_constraints(x + y >= 1000, name="c")
m.add_objective(3 * x + 5 * y, scaling=1e-3)

m.solve(solver_name="highs", output_flag=False)
print("m.objective.value =", m.objective.value)
```

Output (trimmed):

```
linopy.constants:  Optimization successful: 
Status: ok
Termination condition: optimal
Solution: 2 primals, 1 duals
Objective: 3.00e+00
Solver: highs
...
m.objective.value = 3000.0
```

### Expected Behavior

The log reports the objective in model units, i.e. `Objective: 3.00e+03`, consistent with `m.objective.value`. Either unscale before `result.info()` (and the dual bound alongside), or label the logged value as the scaled solver objective.

### Installed Versions

<details>

linopy 0.10.1, highspy (HiGHS) via PyPI, xarray 2026.7.0, numpy 2.4.6, Python 3.12.3

</details>

