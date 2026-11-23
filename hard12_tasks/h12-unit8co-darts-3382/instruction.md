You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] TimeSeries.slice() silently drops in-range points on integer-indexed series with step > 1 when start_ts / end_ts are not in the index

**Describe the bug**
For integer-indexed series (`RangeIndex`) with a step > 1, `TimeSeries.slice(start_ts, end_ts)` silently returns too few points (and sometimes an empty series) when `end_ts` and/or `start_ts` are not part of the time index.

The docstring says that for a `RangeIndex`, `end_ts` is exclusive, so the result should contain every time step `t` with `start_ts <= t < end_ts`. Instead, the last valid point(s) are dropped without any error or warning. The DatetimeIndex branch of the same method does not have this problem (it filters by value), so the same logical slice gives different results depending on the index type.

**To Reproduce**
```python
import numpy as np
import pandas as pd
from darts import TimeSeries

# integer-indexed series with step 2: time index 0, 2, 4, ..., 38
series = TimeSeries.from_times_and_values(pd.RangeIndex(0, 40, 2), np.arange(20.0))

# docstring: for a RangeIndex, `end_ts` is exclusive -> expect all points with start_ts <= t < end_ts
for start, end in [(4, 10), (4, 9), (3, 7), (0, 1), (4, 11)]:
    got = list(series.slice(start, end).time_index)
    expected = [t for t in series.time_index if start <= t < end]
    print(f"slice({start}, {end}): got {got}, expected {expected}" + ("" if got == expected else "   <-- WRONG"))
```

Output:
```
slice(4, 10): got [4, 6, 8], expected [4, 6, 8]
slice(4, 9): got [4, 6], expected [4, 6, 8]   <-- WRONG
slice(3, 7): got [4], expected [4, 6]   <-- WRONG
slice(0, 1): got [], expected [0]   <-- WRONG
slice(4, 11): got [4, 6, 8], expected [4, 6, 8, 10]   <-- WRONG
```

`slice(0, 1)` on a series that starts at `0` returns an **empty** series. The equivalent slices on a DatetimeIndex series with `freq="2D"` return all expected points (inclusive end, as documented).

**Expected behavior**
`slice(start_ts, end_ts)` on a `RangeIndex` series should return all time steps `t` with `start_ts <= t < end_ts`, whether or not `start_ts` / `end_ts` are on the index grid, e.g. `slice(4, 9) -> [4, 6, 8]` and `slice(0, 1) -> [0]`.

**System (please complete the following information):**
 - Python version: 3.12.16 (Windows)
 - darts version: 0.48.1 and `master` (e679f7b)
 - pandas 3.1.1, numpy 2.5.4

**Additional context**
*Root cause:* in the integer branch of `TimeSeries.slice()` (`darts/timeseries.py`), an off-grid `end_ts` is replaced by the *closest* time step (`min(self._time_index, key=lambda t: abs(t - end_ts))`), which is then used as the **exclusive** stop of `pd.RangeIndex(effective_start_ts, effective_end_ts, step=self.freq)`. Whenever that closest step is below `end_ts` (or a tie is broken towards the lower one), a point with `t < end_ts` is excluded. The correction `if end_ts >= effective_end_ts + self.freq` only applies when `end_ts` is beyond the end of the series. The start side was fixed in #1498, but the end side kept the "closest point" logic.

*Possible fix:*
```python
start_idx = self._time_index.searchsorted(start_ts, side="left")
end_idx = self._time_index.searchsorted(end_ts, side="left")
return self[start_idx : max(start_idx, end_idx)]
```
With this change the snippet above returns the expected results, and `test_timeseries.py`, `test_timeseries_multivariate.py`, `test_timeseries_static_covariates.py` and `utils/test_utils.py` pass, except for one assertion in `helper_test_slice` that currently encodes the dropped point:
```python
idx = pd.RangeIndex(start=0, stop=60, step=2)
ts = TimeSeries(idx, values)
slice_vals = ts.slice(11, 31).values(copy=False).flatten()
np.testing.assert_equal(slice_vals, values[6:15])  # times 12..28; 30 < 31 is excluded
```
With an exclusive `end_ts = 31`, time step `30` should be included (`values[6:16]`). Could you confirm the intended semantics? The docstring is also inconsistent: the summary says "ending before `end_ts`", while *Returns* says "smaller or equal than `end_ts`".

Related integer-index fixes: #1498 (start side of `slice()`), #3220 (`slice_n_points_after/before`), #3219 (`longest_contiguous_slice`), #3215 (`extract_subseries`). `split_after`/`split_before`/`drop_after`/`drop_before` raise an explicit `ValueError` for off-grid integer points, whereas `slice()` silently returns wrong data.

I'd be happy to open a PR with the fix and tests once this is approved.

I used an AI assistant (Claude Opus) paired with github api to help investigate; I reproduced and verified it myself.
