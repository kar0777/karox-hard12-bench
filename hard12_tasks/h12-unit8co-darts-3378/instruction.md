You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] qr() (Quantile Risk) triggers runtime warning and returns NaN for zero-sum target series

### Describe the bug

When evaluating probabilistic forecasts with `qr()` (Quantile Risk) on a target series whose values sum to zero ($Z = \sum_{t=1}^T y_t = 0$, such as zero-mean series, intermittent demand with no positive values in the window, or constant zero series), `qr()` executes raw division `losses / z_true` at line 3042.

This triggers an unhandled `RuntimeWarning: invalid value encountered in divide` and returns `NaN` even for a **100% accurate, perfect probabilistic forecast**.

Every other ratio/percentage metric in Darts (`mape`, `smape`, `mase`, `rmsse`, `ope`, `r2_score`, `coefficient_of_variation`) was standardized under #3122, #3132, and #3225 to use `_safe_divide()` with a `zero_division` parameter (`"warn"` or `"raise"`). `qr()` appears to have been overlooked during that migration.

### To Reproduce

```python
import numpy as np
from darts import TimeSeries
from darts.metrics import qr

# Net zero sum series: sum([1.0, -1.0]) = 0.0
actual = TimeSeries.from_values(np.array([1.0, -1.0]).reshape(2, 1, 1))

# Perfect probabilistic prediction matching actual: shape (2 timesteps, 1 component, 2 samples)
pred_perfect = TimeSeries.from_values(np.array([[[1.0, 1.0]], [[-1.0, -1.0]]]))

# Triggers RuntimeWarning: invalid value encountered in divide and returns nan
score = qr(actual, pred_perfect)
print("QR Score:", score)  # nan (expected 0.0)
```

### Expected behavior

`qr()` should accept `zero_division: str = "warn"` and use `_safe_divide()`:
- Under `zero_division="warn"` (default): return `0.0` (ideal risk score) for a perfect forecast ($0/0$) with a logged warning, and `NaN` for non-zero losses on zero scale.
- Under `zero_division="raise"`: raise `ValueError`.

### Proposed Fix

I have this fixed and tested locally:
1. Added `zero_division: str = "warn"` to `qr()` in `darts/metrics/metrics.py`.
2. Routed denominator division through `_safe_divide(losses, z_true, zero_division=zero_division, zero_fill=0.0, strict_zero=True, metric_type="percentage")`.
3. Added unit tests in `test_metrics.py` covering zero-actual with perfect/imperfect forecasts, exception raising, multi-component isolation, and multi-quantiles (all 488 metrics tests pass).

Happy to open the PR once approved!
