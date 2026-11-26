You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`remove_variables` deletes unrelated constraints: `-1` means "masked" in a variable but "empty term slot" in a constraint

### Version Checks (indicate both or one)

- [x] I have confirmed this bug exists on the lastest [release](https://github.com/pypsa/linopy/releases) of Linopy.

- [x] I have confirmed this bug exists on the current [`master`](https://github.com/pypsa/linopy/tree/master) branch of Linopy.


### Issue Description

## Summary

Since 0.8, `Model.remove_variables(name)` deletes every constraint for which `Constraint.has_variable(variable)` is true. That test is

```python
# linopy/constraints.py
def has_variable(self, variable: variables.Variable) -> bool:
    return bool(self.data["vars"].isin(variable.labels.values.ravel()).any())
```

`-1` appears on both sides of that comparison with two unrelated meanings:

- in `variable.labels`, `-1` marks an entry masked out by `mask=`;
- in `constraint.data["vars"]`, `-1` marks an unused term slot in the padded  `_term` dimension.

So **any masked variable tests as "used by" any constraint that has a padded term slot**, and removing the former silently deletes the latter. Models that use `mask=` at all are affected, and the more masking there is, the more constraints are destroyed.

The failure is quiet: the model still builds, it has simply lost constraints, so it typically goes on to solve unbounded or to a wrong optimum. The emitted `UserWarning` names constraints that genuinely have nothing to do with the removed variable, which makes it read like a false alarm rather than a symptom.

### Reproducible Example

```python
import pandas as pd
import xarray as xr
import linopy
from linopy import Model

print("linopy", linopy.__version__)

idx = pd.Index([0, 1, 2], name="i")
m = Model()

a = m.add_variables(
    name="a", lower=0, coords=[idx],
    mask=xr.DataArray([True, False, True], coords=[idx]),
)
b = m.add_variables(
    name="b", lower=0, coords=[idx],
    mask=xr.DataArray([True, True, False], coords=[idx]),
)

m.add_constraints(b >= 1, name="only_b")

print("a labels   :", a.labels.values)                                  # [ 0 -1  2]
print("b labels   :", b.labels.values)                                  # [ 3  4 -1]
print("only_b vars:", m.constraints["only_b"].data["vars"].values.ravel())  # [ 3  4 -1]

m.remove_variables("a")
print("only_b still in model:", "only_b" in m.constraints)
```

### Expected Behavior

`only_b` should survive: it does not use `a`. More generally, `has_variable` should ignore the `-1` sentinel on both sides.


## Suggested fix

Restrict the membership test to real labels:

```python
def has_variable(self, variable: variables.Variable) -> bool:
    labels = variable.labels.values.ravel()
    labels = labels[labels >= 0]
    used = self.data["vars"]
    return bool(used.where(used >= 0).isin(labels).any())
```

(or filter `used` to `>= 0` first — the point is that neither side should let `-1` match `-1`.)


### Installed Versions

<details>
- linopy 0.7.0 (correct), 0.8.0 and 0.9.0 (both affected)
- Python 3.13, xarray 2025.12.0, pandas 2.x
</details>

