You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

BUG: Censored discrete distributions with integer bounds fail logprob derivation since 6.2.0 (find_measurable_clips builds a type-mismatched replacement)

## Description

Since 6.2.0, `pm.Censored` over a **discrete** distribution fails logprob derivation whenever the bounds or observed values are integers — which is the natural dtype for them. Continuous distributions are unaffected. Bisects to the censoring rework in #8363 (merged 2026-07-19, released in 6.2.0); still present on current `main`.

The failure is effectively unavoidable from the user side: passing integer observations doesn't help, because pymc's own observed-data handling converts them to float64, which the rewrite then rejects against the integer graph. The only working form is casting **both** `upper` and `observed` to float yourself, which a user has no way to discover.

```python
import numpy as np
import pymc as pm

with pm.Model() as m:
    pm.Censored("y", pm.Poisson.dist(3), lower=None, upper=np.full(10, 5), observed=np.full(10, 3))
    m.logp()
# RuntimeError: The logprob terms of the following value variables could not be derived: ...
```

With `pytensor.config.exception_verbosity` raised, the underlying rewrite failure is visible:

```
<<!! BUG IN FGRAPH.REPLACE OR A LISTENER !!>> <class 'TypeError'>
Cannot convert Type Vector(int64, shape=(10,)) (of Variable MeasurableClip.0)
into Type Vector(float64, shape=(10,)). ... find_measurable_clips
```

Behavior matrix on 6.2.0 (all pass on 6.0.x):

| case | result |
|---|---|
| Censored **continuous** (Normal), any dtype mix | OK |
| Censored **discrete** (Poisson), float upper & observed | OK |
| Censored **discrete** (Poisson), integer upper and/or observed | **RuntimeError** |

## Cause

A dtype disagreement between the node built by `pm.Censored` and the replacement built by `find_measurable_clips`:

1. `Censored` with `lower=None` compiles to `clip(rv, -inf, upper)`. The float `-inf` promotes the **original Clip node to float64** even for an int64 base RV, and the value variable is created to match (float64).
2. The reworked `find_measurable_clips` deliberately uses the base variable as the unbounded sentinel — the comment says *"unlike +-inf constants, it does not upcast discrete variables"* — so the **replacement `MeasurableClip` comes out int64**.
3. `fgraph.replace` correctly refuses the float64 → int64 substitution, the rewrite dies, no measurable node exists, and `conditional_logp` raises the generic `RuntimeError`.

Neither half is wrong in isolation; the replacement just isn't type-preserving against the node it replaces.

## Proposed fix

Reuse #8363's own idiom (emit the explicit op, let the existing rewrite claim it on a later pass), applied to promoted clips — when the measurable clip's dtype differs from the original node's, relabel it with an explicit widening cast and let `find_measurable_casts` claim it as measure-preserving:

```diff
     clipped_rv = (
         MeasurableClip(scalar_clip).make_node(base_var, lower_bound, upper_bound).outputs[0]
     )
+
+    [old_out] = node.outputs
+    if clipped_rv.type.dtype != old_out.type.dtype:
+        # The +-inf sentinel in the original graph upcast a discrete base; the
+        # measurable clip preserves the base dtype instead, so relabel it with an
+        # explicit cast and let find_measurable_casts claim the widening cast as
+        # measure-preserving on a later pass.
+        clipped_rv = pt.cast(clipped_rv, old_out.type.dtype)
+
     return [clipped_rv]
```

## Verification of the fix

Applied to 6.2.0 and compared against a pymc 6.0.1 reference environment — **bit-identical logp on every probe**, including edge cases:

- interior observation: exactly `n * poisson.logpmf(3, 3)`; observation at the censor point: exactly the survival mass `n * log P(X >= 5)`
- non-integral observed below the bound and at a non-integral censor point: identical to 6.0.1 (pymc's discrete logps evaluate the formula without integrality checks — pre-existing behavior, unchanged by this fix)
- latent (unobserved) censored discrete variable: identical
- partially `-inf` lower-bound vector: identical (that path keeps a float bound and never fires the new branch)
- censored continuous distributions: unaffected (dtypes already agree)

Not exercised: the clip-of-clip fusion branch on `main` (the patch compares against `node.outputs[0]`, so it should compose, but a test would be good) and `floatX="float32"`.

Happy to open a PR with the patch plus regression tests if the approach looks right.

## Context

Found while bumping pymc-marketing to pymc 6.2 (pymc-labs/pymc-marketing#2803): our `ShiftedBetaGeoModel` is a `Censored(ShiftedBetaGeometric, upper=T)` with integer `T` — every test of that model broke. Downstream we work around it by casting `upper`/`observed` to float, which behaves identically on 6.0/6.2/main.

## Versions

- pymc 6.2.0 (also reproduced on main @ `9e94b48`)
- pytensor 3.2.4, numpy 2.4.6, python 3.13, macOS/Linux

