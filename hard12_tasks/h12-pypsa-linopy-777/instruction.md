You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

LP file export silently drops per-element bounds on binary variables, diverging from direct API

There is a discepancy betwenn `io_api="direct"` and `io_api="lp"` when in comes to bounds of binaries. The API should be consistent

> [!NOTE]
> This issue was drafted with AI assistance (Claude Code); content reviewed before posting.

### Version Checks (indicate both or one)

- [x] I have confirmed this bug exists on the latest [release](https://github.com/pypsa/linopy/releases) of Linopy (v0.8.0).

### Issue Description

Per-element bounds set on a **binary** variable are honored by the direct/matrix solver path but silently dropped by the LP file export, so the same model has different feasible sets depending on `io_api`.

- `matrices._build_vars` collects `var.lower`/`var.upper` for *all* variables, including binaries, and these `lb`/`ub` flow into the direct solver interfaces (e.g. gurobipy `setAttr("LB"/"UB", ...)`).
- `io.bounds_to_file` writes bound rows only for `continuous + integers + semi_continuous`, plus binaries with `Variable.fixed == True` (whole-variable `.fix()`, added in #773). Binaries otherwise only appear in the `binary` section, which implies `[0, 1]` — any tighter per-element bounds (e.g. masking out a subset of entries with `upper = 0`) are silently lost.

This is longstanding behavior (not a 0.8.0 regression — before #773 binaries got no bound rows at all), but the divergence between the two paths is a silent correctness trap: a model that is correct with `io_api="direct"` relaxes when solved through an LP file.

Suggested fix: in `bounds_to_file`, also include binary variables whose bounds differ anywhere from `(0, 1)` — the LP format's bounds section may further restrict variables declared binary, and Gurobi/HiGHS honor this. Alternatively (or additionally), warn on LP export when a binary variable carries non-default bounds.

### Reproducible Example

```python
import pandas as pd
import linopy

m = linopy.Model()
x = m.add_variables(binary=True, coords=[pd.RangeIndex(4, name="t")], name="x")
x.upper = pd.Series([1, 1, 0, 0], index=pd.RangeIndex(4, name="t"))  # forbid x at t=2,3
m.add_constraints(x.sum() >= 2, name="atleast2")
m.add_objective(-1 * x.sum())

print(m.matrices.ub)  # [1 1 0 0] -> direct API honors the bounds, optimum -2

m.to_file("model.lp")
print(open("model.lp").read())
# LP file contains no bounds section at all; all four variables only appear
# under `binary` (implied [0,1]) -> LP-based solve returns optimum -4
```

### Expected Behavior

Both solver paths see the same feasible set: the LP file should contain

```
bounds
0 <= x2 <= 0
0 <= x3 <= 0
```

(or the export should at least warn that non-default bounds on a binary variable are being dropped).

### Installed Versions

<details>

linopy 0.8.0, python 3.12, linux

</details>

