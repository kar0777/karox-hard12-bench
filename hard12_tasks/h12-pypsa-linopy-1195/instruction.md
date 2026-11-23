You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

sparse: adding a linear to a quadratic expression densifies it and warns the user

> [!NOTE]
> This issue was drafted by AI (Claude) and reviewed before posting.

### Version Checks
- [x] I have confirmed this bug exists on the current `master` branch of Linopy (912a8c9b).

### Issue Description

On a sparse model, adding a CSR-backed linear expression to a quadratic expression densifies the linear one. Quadratic products have no sparse backing, and `LinearExpression.to_quadexpr` reads `self.data`. linopy then emits `PerformanceWarning: Sparse (CSR) backing densified: data(read).`

Any model with a linear plus a quadratic objective term hits this. In PyPSA, which now builds sparse by default (PyPSA/PyPSA#2141), every network with `marginal_cost_quadratic` triggers it inside `Model.from_spec`. The user cannot act on the warning, because the densifying happens in linopy's own spec build.

#972 listed quadratic products as out of scope for the CSR path, "revisit them if users report them". This is that report.

### Reproducible Example

```python
import warnings
import pandas as pd
import linopy

warnings.simplefilter("always")
m = linopy.Model(sparse=True)
x = m.add_variables(coords=[pd.RangeIndex(1000, name="i")], name="x")
lin = (2 * x).sum()
quad = (x * x).sum()
print(lin.is_sparse, quad.is_sparse)  # True False

with warnings.catch_warnings(record=True) as w:
    m.add_objective(2 * x + x * x)
print([str(i.message) for i in w])
# ['Sparse (CSR) backing densified: data(read).']
```

### Expected Behavior

One of these, in order of preference:

1. Quadratic expressions get a sparse backing, so `linear + quadratic` stays sparse.
2. `to_quadexpr` keeps the CSR terms and pads the `_factor` dim without going through the dense `data` read.
3. At least, a densifying that linopy does internally (e.g. inside `from_spec` or `add_objective`) does not warn the user, who cannot avoid it.

### Installed Versions

<details>

- linopy 0.10.0.post1.dev106+g912a8c9bf
- Python 3.12, Linux

</details>

