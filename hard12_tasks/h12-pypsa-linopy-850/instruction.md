You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

v1: legacy alignment warning fires on @/dot even when operands are exactly aligned

> 🤖 _This issue was written by Claude (Claude Code), based on hands-on findings while migrating PyPSA to the v1 arithmetic semantics. Reproductions were verified against the PR #717 branch._

## Summary

The legacy alignment `LinopySemanticsWarning` fires on `@` / `dot` **even when the operands are already exactly aligned** (identical coordinate labels *and* order) on the contracted dimension. v1 accepts the same expression without complaint and both produce identical results, so the legacy warning appears to be a false positive for the aligned case.

## Reproduction

`linopy 0.8.0.post1.dev123+g5a131a628` (branch `feat/arithmetic-convention`), Python 3.12:

```python
import warnings, numpy as np, pandas as pd, xarray as xr
import linopy as ln
from linopy.config import LinopySemanticsWarning

m = ln.Model()
names = pd.Index(["a", "b", "c"], name="name")
sns   = pd.Index([0, 1, 2], name="snapshot")
x = m.add_variables(coords=[sns, names], name="x")
C = xr.DataArray(np.ones((3, 2)), dims=["name", "cyc"],
                 coords={"name": names})          # same labels + order as x

for sem in ["legacy", "v1"]:
    ln.options["semantics"] = sem
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        x @ C
        warned = any(issubclass(a.category, LinopySemanticsWarning) for a in w)
        print(sem, "->", "WARN" if warned else "ok")
```

```
legacy -> WARN
v1     -> ok
```

The `name` coordinate is identical on both operands (same labels, same order); the contraction is unambiguous. v1 accepts it and the resulting expression matches legacy's.

## Why it matters

This showed up in PyPSA's Kirchhoff voltage law constraint (`flow @ C_branch`). After I aligned the operands' `name` coordinates so v1 would accept the expression, **v1 passed but legacy still warned** at the same line — and with `LinopySemanticsWarning` subclassing `FutureWarning`, downstreams that treat `FutureWarning` as an error get churn on code that is already correct under both semantics.

## Suggestion

Scope the legacy alignment warning on `@` / `dot` (and, if applicable, the reductions that share this path) to *actual* divergence — i.e. don't warn when the operands are already exactly aligned on the shared/contracted dimension, since there is nothing for the caller to change.

