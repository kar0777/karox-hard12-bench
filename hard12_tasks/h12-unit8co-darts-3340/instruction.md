You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

FourTheta.fit and Theta.fit fail with ValueError on non-positive series under default SeasonalityMode.MULTIPLICATIVE

### Describe the bug

When fitting `FourTheta()` or `Theta()` with the default `season_mode=SeasonalityMode.MULTIPLICATIVE` on a `TimeSeries` that contains zero or negative values (`(ts.values() <= 0).any()`), `fit()` raises:

```
ValueError: Multiplicative seasonality is not appropriate for zero and negative values
```

Notably, `FourTheta.select_best_model()` (`darts/models/forecasting/theta.py`, lines 495–502) already checks `if (ts.values(copy=False) <= 0).any():` and falls back to additive seasonality (`season_mode = [SeasonalityMode.ADDITIVE]`), additive model (`model_mode = [ModelMode.ADDITIVE]`), and linear trend (`drift_mode = [TrendMode.LINEAR]`):

```python
if (ts.values(copy=False) <= 0).any():
    drift_mode = [TrendMode.LINEAR]
    model_mode = [ModelMode.ADDITIVE]
    season_mode = [SeasonalityMode.ADDITIVE]
    logger.warning(
        "Time series has negative or zero values. Only additive modes and linear trend will be tested."
    )
```

However, in `FourTheta.fit()` (lines 353–367):
1. `extract_trend_and_seasonality(new_ts, self.season_period, model=self.season_mode)` is called at **line 354** *before* checking `if (ts_values <= 0).any():` at **line 362**.
2. Even at line 362, `FourTheta.fit()` only falls back `self.model_mode = ModelMode.ADDITIVE` and `self.trend_mode = TrendMode.LINEAR`, without falling back `self.season_mode = SeasonalityMode.ADDITIVE`.

Similarly, `Theta.fit()` (lines 130–135) calls `extract_trend_and_seasonality(ts, self.season_period, model=self.season_mode)` without falling back to `SeasonalityMode.ADDITIVE` when `(ts.values(copy=False) <= 0).any()`.

### To Reproduce

```python
import numpy as np
import pandas as pd
from darts import TimeSeries
from darts.models import FourTheta, Theta

dates = pd.date_range("2023-01-01", periods=36, freq="MS")
values = np.sin(np.linspace(0, 6 * np.pi, 36)) + 1.0
values[5] = 0.0  # Common in intermittent / retail demand series
ts = TimeSeries.from_times_and_values(dates, values)

# Both fail with ValueError: Multiplicative seasonality is not appropriate for zero and negative values
FourTheta(seasonality_period=12).fit(ts)
Theta(seasonality_period=12).fit(ts)
```

### Expected behavior

In both `FourTheta.fit()` and `Theta.fit()`, the check `if (ts.values(copy=False) <= 0).any():` should run **before** `extract_trend_and_seasonality(...)`, and if `self.season_mode is SeasonalityMode.MULTIPLICATIVE`, it should automatically fall back to `SeasonalityMode.ADDITIVE` with a warning (consistent with `FourTheta.select_best_model()` and `FourTheta.fit()`'s existing fallback for `model_mode` and `trend_mode`).

### System Info

- Darts version: `0.48.1`
- Python version: `3.12`

