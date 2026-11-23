You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] FFT never aligns weekly seasonality: `"weekday"` resolves to a method on `pd.Timestamp`

## Descripción

**Describe the bug**

When `FFT` detects weekly seasonality (daily series, or hourly series with a weekly pattern), `_find_relevant_timestamp_attributes()` returns `{"weekday"}` (`darts/models/forecasting/fft.py`, lines 117 and 127). `_compare_timestamps_on_attributes()` then compares `getattr(ts_1, "weekday") == getattr(ts_2, "weekday")`, but on a `pd.Timestamp`, `weekday` is a **method**, not a property. Two bound methods of different timestamps never compare equal, even when both dates fall on the same day of the week, so `_crop_to_match_seasons()` never finds a matching timestamp. It logs `"No matching timestamp could be found, returning original TimeSeries."` and fits on the uncropped series, so the weekly seasonal phase is not aligned with the forecast start.

The same happens when a user passes `required_matches={"weekday"}`.

**To Reproduce**

```python
import numpy as np
import pandas as pd
from darts import TimeSeries
from darts.models import FFT

idx = pd.date_range("2024-01-01", periods=73, freq="D")
pattern = np.array([1, 2, 3, 4, 5, 10, 12], dtype=float)
ts = TimeSeries.from_times_and_values(idx, np.tile(pattern, 11)[: len(idx)])
truth = np.roll(pattern, -(len(idx) % 7))

for required_matches in [None, {"day_of_week"}]:
    model = FFT(required_matches=required_matches)
    model.fit(ts)
    pred = model.predict(7).values().ravel()
    print(required_matches, "MAE:", np.abs(pred - truth).mean())
```

Output (darts `master`, pandas 3.1.0):

```text
No matching timestamp could be found, returning original TimeSeries.
None MAE: 3.687
{'day_of_week'} MAE: 1.94
```

```python
>>> a, b = pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-08")  # both Mondays
>>> getattr(a, "weekday") == getattr(b, "weekday")
False
>>> getattr(a, "day_of_week") == getattr(b, "day_of_week")
True
```

**Expected behavior**

With the default `required_matches=None`, weekly seasonality is detected and the training series is cropped to match the day of the week of the first prediction point.

**Proposed fix**

Use the `day_of_week` property instead of `"weekday"` in `_find_relevant_timestamp_attributes()` (lines 117 and 127), and update the `test_fft.py` expectations accordingly. Optionally, `_compare_timestamps_on_attributes()` could raise a clear error if an attribute in `required_matches` is not a property (e.g. callable), so that user-provided `required_matches={"weekday"}` doesn't fail silently.

I'd be happy to open a PR for this.

**System:**
- Python version: 3.13
- darts version: `master` (0.48.1)
- pandas: 3.1.0 (also affects pandas 2.x, since `Timestamp.weekday` has always been a method)
