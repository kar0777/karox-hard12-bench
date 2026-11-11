You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Warn or provide aggregation parameter in TimeSeries.values() / to_dataframe() when called on stochastic TimeSeries (n_samples > 1)

### Problem Description

When calling `ts.values()` or `ts.to_dataframe()` on a stochastic `TimeSeries` (`ts.n_samples > 1`), Darts silently returns **only the first Monte Carlo sample (`sample 0`)**:

```python
# darts/timeseries.py
def values(self, copy: bool = True, sample: int = 0) -> np.ndarray:
    if self.is_Deterministic:
        return np.copy(self._values[:, :, 0]) if copy else self._values[:, :, 0]
    return np.copy(self._values[:, :, sample]) if copy else self._values[:, :, sample]
```

While the docstring notes that `sample: int = 0` defaults to the first sample, this is a frequent footgun in production pipelines:
- Calling `pred.values()` or `pred.to_dataframe()` on a probabilistic forecast (`num_samples=200`) silently extracts a single random Monte Carlo trajectory (`sample=0`) rather than a central point estimate (such as the median `quantile(0.5)` or mean `mean()`), without raising a warning.
- Downstream code expecting a 2D array `(n_timesteps, n_components)` of point forecasts ends up evaluating or exporting a noisy single draw, which can degrade accuracy metrics (e.g., MAPE/WAPE) or cause inconsistent results across runs.

### Proposed Improvement

Consider one or both of the following improvements:
1. **Emit a warning** (or provide an optional `agg: str | float | None` parameter in `values()` / `to_dataframe()`) when `values()` / `to_dataframe()` is called on a stochastic `TimeSeries` (`n_samples > 1`) without an explicit `sample` argument.
2. **Support `agg="median"` / `agg="mean"` (or `quantile=0.5`)** directly in `values()` / `to_dataframe()`, or recommend `ts.quantile(0.5).values()` / `ts.mean().values()` in the warning message so users do not accidentally use `sample=0` as a point forecast.

