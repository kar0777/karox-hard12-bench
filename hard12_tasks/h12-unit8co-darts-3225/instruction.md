You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] r2_score is outside the zero_division design from #3132: a constant actual series scores NaN for a perfect forecast

**Describe the bug**

`r2_score` divides by its denominator without a guard (`darts/metrics/metrics.py:2508-2511`):

```python
ss_errors = np.nansum((y_true - y_pred) ** 2, axis=TIME_AX)
y_hat = np.nanmean(y_true, axis=TIME_AX)
ss_tot = np.nansum((y_true - y_hat) ** 2, axis=TIME_AX)
return 1 - ss_errors / ss_tot
```

`ss_tot` is zero whenever the actual series is constant, which is a normal thing to score: a flat segment, a sensor that did not move, a zero-inflated series.

#3132 records the agreed design for exactly this situation:

> * **0/0** (numerator 0 *and* denominator 0) → the metric's **best score** (a perfect forecast on a degenerate series)
> * **x/0** (numerator != 0, denominator 0) → `np.nan`. Filling with the best score here would mask a real miss.
> * `zero_division="raise"` preserves the legacy `ValueError`.

`r2_score` matches neither branch:

| case | agreed design | `r2_score` today | `sklearn.metrics.r2_score` |
|---|---|---|---|
| constant actual, exact forecast (0/0) | best score, i.e. `1.0` | `nan` | `1.0` |
| constant actual, wrong forecast (x/0) | `nan` | `-inf` | `0.0` |

It also does not accept `zero_division`, while `mape`, `ape`, `arre`, `marre`, `ope`, `wmape` and `coefficient_of_variation` all do.

Neither #3132 nor #3080 mentions R^2; the work was scoped to the percentage and range metrics, and `r2_score` appears to have been missed rather than deliberately excluded.

**To Reproduce**

```python
import numpy as np, pandas as pd
from darts import TimeSeries, metrics

ts = lambda v: TimeSeries.from_series(pd.Series(np.array(v, float), index=pd.RangeIndex(len(v))))

# a forecast that is exactly right, on a constant series
print(metrics.r2_score(ts([5., 5., 5., 5.]), ts([5., 5., 5., 5.])))   # nan
# a forecast that is wrong, on the same series
print(metrics.r2_score(ts([5., 5., 5., 5.]), ts([1., 2., 3., 4.])))   # -inf

metrics.r2_score(ts([5., 5., 5., 5.]), ts([5., 5., 5., 5.]), zero_division="raise")
# TypeError: r2_score() got an unexpected keyword argument 'zero_division'
```

**Expected behavior**

The design already agreed in #3132, applied to `r2_score`: route the division through the shared `_safe_divide` helper (`darts/metrics/utils.py:876`) and accept `zero_division` as the sibling metrics do. Note that the helper divides `ss_errors` by `ss_tot`, so the fill applies to the ratio rather than to R^2 itself: `zero_fill=0.0` is the value that makes the 0/0 case come out as R^2 = 1.0, the best score. `strict_zero=True` also looks right here, so that a genuinely small variance is not treated as zero. That gives `1.0` for the exact forecast, `nan` for the wrong one, and `ValueError` under `zero_division="raise"`, and it happens to agree with `sklearn` on the first two.

**Additional context**

Also reaches `backtest` and `gridsearch` when `metric=r2_score`, since one constant window makes the aggregate `nan` or `-inf`.

I have a fix and regression tests ready and would be happy to open the PR, if this reading of #3132 is the one you intended.

**System**

```
darts 0.47.0 (master @ 351b53e1) | python 3.13.3 | pandas 3.0.6 | numpy 2.5.3 | Linux x86_64
```

LLM generated content, by Claude Opus 5. The measurements were produced with it; the contributor reviewed them.


