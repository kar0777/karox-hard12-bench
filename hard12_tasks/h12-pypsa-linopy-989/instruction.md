You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

v1: solve-time coordinate check rejects models with independent label sets on a shared dimension (breaks PyPSA)

> [!NOTE]
> This issue was drafted with AI assistance.

### Version Checks (indicate both or one)

- [ ] I have confirmed this bug exists on the latest release of Linopy.
- [x] I have confirmed this bug exists on the current `master` branch of Linopy.

### Issue Description

Since #955, `Model.solve()` runs `_check_coord_consistency()` under `semantics="v1"`. It raises when two containers share a dimension name but their labels do not nest.

PyPSA uses one dimension `name` for all components (`Generator-p`, `Store-e`, `Bus-nodal_balance`, ...), each with its own disjoint labels. So every PyPSA model with more than one component type fails at solve time under v1. Running PyPSA master tests (`test_lopf_storage`, `test_lopf_multiinvest`, `test_optimization_expressions`, `test_components_store`) with `LINOPY_SEMANTICS=v1` against linopy master gives 42 of 148 failed, all with this error.

These variables are never combined element-wise, so no ambiguous alignment happens. The model is valid.

### Reproducible Example

```python
import linopy
import pandas as pd

linopy.options["semantics"] = "v1"

m = linopy.Model()
gen = m.add_variables(lower=0, coords=[pd.Index(["gen1", "gen2"], name="name")], name="Generator-p")
store = m.add_variables(lower=0, coords=[pd.Index(["store1"], name="name")], name="Store-e")
m.add_constraints(gen.sum() + store.sum() >= 1, name="balance")
m.add_objective(gen.sum() + store.sum())
m.solve()
```

```
ValueError: Coordinates for dimension 'name' are incompatible across the model: 'Store-e' carries labels not contained in the largest carrier 'Generator-p', so they are neither equal nor subsets of a shared index. Use Model.assign_coords to relabel the model, or align the containers with `.sel`.
```

### Expected Behavior

The model solves, as under legacy semantics. Containers that share a dimension name without being combined should not need identical or nested labels. Alternatively, v1 should document how downstream packages like PyPSA should model independent label sets on a shared dimension name, before the check becomes a hard error.

### Installed Versions

- linopy 0.9.1.post1.dev42+g7f06ffaf1 (master, 7f06ffaf)
- xarray 2026.7.0
- pandas 3.0.3
- python 3.13.11

