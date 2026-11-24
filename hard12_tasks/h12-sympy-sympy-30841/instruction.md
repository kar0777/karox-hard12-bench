You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

singularities() fails on 0**exp for bounded domains and disconnected solution sets, and misses poles for variable-exponent powers

### Problem Description

In `sympy.calculus.singularities.singularities`, handling of `Pow` expressions contains multiple issues:

#### 1. Crash on `0**exp` when exponent is strictly positive on a subdomain
When querying `singularities(0**(x - 1), x, Interval(2, 5))`, `solveset(i.exp <= 0, symbol, domain)` evaluates to `EmptySet`.
The function then calls:
```python
sing_interval = Interval.open(sing_interval.inf, sing_interval.sup)
```
Calling `EmptySet.inf` raises `NotImplementedError: (EmptySet)._inf`, which causes `singularities()` to fail with `NotImplementedError: Methods for determining the singularities of this function have not been developed.`
This consequently causes `continuous_domain(0**(x - 1), x, Interval(2, 5))` to crash with `NotImplementedError` even though the expression is constant 0 and continuous across `[2, 5]`.

#### 2. Disconnected solution sets for `0**exp` corrupted to `Interval(-oo, oo)`
For `0**(1 - x**2)` on `S.Reals`, the exponent is negative on `(-oo, -1) U (1, oo)`. Because `singularities()` calls `Interval.open(sing_interval.inf, sing_interval.sup)`, taking the infimum and supremum evaluates to `-oo` and `oo`, wiping out the valid domain and returning `Interval(-oo, oo)`.
This marks the entire interval `(-1, 1)` as singular and causes `continuous_domain(0**(1 - x**2), x, S.Reals)` to return `EmptySet`.

#### 3. Missed poles for powers with variable exponents
In `singularities.py`:
```python
if i.exp.is_negative:
    # XXX: exponent of varying sign not handled
    sings += solveset(i.base, symbol, domain)
```
When the exponent depends on `symbol` (e.g. `(x - 2)**(x - 3)` or `(x**2 - 4)**(x - 1)`), `i.exp.is_negative` evaluates to `None`. The check is skipped entirely, returning `EmptySet` and missing poles (such as `x = 2` for `(x - 2)**(x - 3)` where `0**(-1) = zoo`, and `x = -2` for `(x**2 - 4)**(x - 1)`).

### Reproduction

```python
from sympy import Symbol, Interval, S, singularities
from sympy.calculus.util import continuous_domain

x = Symbol('x', real=True)

# 1. Crashes with NotImplementedError
singularities(0**(x - 1), x, Interval(2, 5))

# 2. Returns Interval(-oo, oo) instead of Union(Interval.open(-oo, -1), Interval.open(1, oo))
singularities(0**(1 - x**2), x)

# 3. Returns EmptySet instead of FiniteSet(2)
singularities((x - 2)**(x - 3), x)
```

### Expected Behavior
1. `singularities(0**(x - 1), x, Interval(2, 5))` -> `EmptySet`
2. `singularities(0**(1 - x**2), x)` -> `Union(Interval.open(-oo, -1), Interval.open(1, oo))`
3. `singularities((x - 2)**(x - 3), x)` -> `FiniteSet(2)`

