You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bug: nested SymbolicRandomVariable inside CustomDist.logp raises 'Random variables detected in the logp graph'

> **Note:** This issue was machine-generated. The bisection and surgical-revert
> check below were each run in disposable containers.

## Summary

`model.logp()` fails for a `pm.CustomDist` whose `logp` builds a nested
`SymbolicRandomVariable` and immediately calls `pm.logp(...)` on it.

The failure started in PyMC 5.28.0 and is still present in 6.0.0. The same
reproducer passes on 5.27.1.

## Minimal reproducer

```python
import numpy as np
import pymc as pm

print(f"pymc: {pm.__version__}")

with pm.Model() as m:
    def logp(value, sigma):
        inner = pm.Truncated.dist(pm.Normal.dist(sigma=sigma), lower=-5.0, upper=5.0)
        outer = pm.Truncated.dist(inner, lower=0.1)
        return pm.logp(outer, value)

    pm.CustomDist(
        "obs",
        np.array([1.0, 1.0, 1.0]),
        logp=logp,
        observed=np.array([0.5, 0.7, 1.0]),
    )

m.logp()
```

## Actual behavior

On PyMC 5.28.0 through 6.0.0, the script raises:

```text
ValueError: Random variables detected in the logp graph:
  {truncated_normal_rv{"(),(),(),()->()"}.out}.
This can happen when mixing variables from different models, or when CustomDist
logp or Interval transform functions reference nonlocal variables.
```

The custom `logp` does not close over any model random variables. The random
variable reported in the error is created inside the `logp` function itself.

## Expected behavior

`m.logp()` should build successfully, as it does on PyMC 5.27.1.

## Version check

I reproduced this against the following PyMC versions:

| PyMC version | Result |
| --- | --- |
| 5.27.1 | passes |
| 5.28.0 | fails |
| 5.28.1-5.28.5 | fails |
| 6.0.0 | fails |

## Reproduction notes

The failure seems to require both of these conditions:

1. The custom `logp` constructs a nested `SymbolicRandomVariable`, such as
   `pm.Truncated.dist(pm.Truncated.dist(...))`. A single
   `pm.Truncated.dist(pm.Normal.dist(...))` did not trigger the error in my
   variants.
2. A vector-shaped parameter is passed through `CustomDist`. A NumPy constant
   is enough; it does not need to be a PyMC random variable.

The error is triggered by `m.logp()`, which is also hit by `pm.sample()` during
step-method selection. Calling `m.compile_logp()(m.initial_point())` alone did
not trigger the same failure in my reduced example.

## Possible regression lead

The regression window points to the 5.28.0 release. One suspicious change is
PR #8105, which added `maybe_resize(class_X(...), size)` around the
`SymbolicRandomVariable` dispatches in `pymc/distributions/distribution.py`.

As a diagnostic only, removing those `maybe_resize(...)` wrappers from the
`logp`, `logcdf`, `logccdf`, and `icdf` dispatches makes this reproducer pass
again on 5.28.5 and 6.0.0. I am not suggesting that as a fix, because it would
presumably regress the broadcasting behavior PR #8105 added. It does suggest
that `size`/shape handling may be pulling an inner RV into the final logp graph
for nested `SymbolicRandomVariable`s.

Reverting only one or two of the four wrappers is not enough — each dispatch
contributes a separate `pt.alloc`, and `Truncated.logp` invokes `logcdf` for
normalisation, so multiple wrappers are exercised per call. A safer fix would
preserve PR #8105's broadcast intent while not embedding `size` references
that hold RV ancestors.

## Related work

- https://github.com/pymc-devs/pymc-extras/issues/673 reported a similar `Random variables detected in the logp
  graph` error through a different reproducer.
- PyMC PR #8274, merged in 5.28.5, does not fix the reproducer above.
- https://github.com/pymc-devs/pytensor/issues/2056 may be related if the underlying issue is shape information
  retaining live RV ancestors.

