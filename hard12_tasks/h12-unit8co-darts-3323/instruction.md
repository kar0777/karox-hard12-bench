You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Add check_stationarity option to granger_causality_tests() to avoid unconditional KPSS InterpolationWarning spam

### Describe the problem

In [`darts.utils.statistics.granger_causality_tests`](https://github.com/unit8co/darts/blob/master/darts/utils/statistics.py#L547-L621), lines 606–613 unconditionally call `stationarity_tests(ts_cause)` and `stationarity_tests(ts_effect)` before running `grangercausalitytests`:

```python
    if not stationarity_tests(ts_cause):
        logger.warning(
            "The series 'ts_cause' is not stationary. Consider differencing it or transforming it before "
            "running the Granger causality test."
        )
    if not stationarity_tests(ts_effect):
        logger.warning(
            "The series 'ts_effect' is not stationary. Consider differencing it or transforming it before "
            "running the Granger causality test."
        )
```

In practice, this causes two issues when users run Granger causality tests across multiple series or lag candidates on **already-detrended / stationary** series:

1. **Massive `InterpolationWarning` spam from KPSS**:
   `stationarity_tests()` calls `stationarity_test_kpss()`, which invokes `statsmodels.tsa.stattools.kpss()`. Whenever a stationary series has a test statistic smaller than the lowest critical value in `statsmodels`' look-up table ($p > 0.10$), `statsmodels` emits:
   ```
   InterpolationWarning: The test statistic is outside of the range of p-values available in the look-up table. The actual p-value is greater than the p-value returned.
   ```
   Because `granger_causality_tests()` calls `stationarity_tests()` twice per invocation, evaluating Granger causality across $N$ candidate covariates or panel series generates hundreds of `InterpolationWarning`s and `logger.warning` messages even when the series are intentionally pre-detrended.
2. **Unnecessary computation overhead**:
   Running ADF (`adfuller`) + KPSS (`kpss`) on both series on every call doubles the execution time when testing bidirectional causality or scanning multiple covariates against the same target series.

### Proposed solution

Add an optional parameter `check_stationarity: bool = True` (and/or `show_warnings: bool = True`, consistent with other Darts functions) to `granger_causality_tests()`:

```python
def granger_causality_tests(
    ts_cause: TimeSeries,
    ts_effect: TimeSeries,
    maxlag: int | Iterable[int],
    addconst: bool = True,
    check_stationarity: bool = True,
    n_jobs: int = 1,
) -> dict:
```

- Default `check_stationarity=True` preserves 100% backward compatibility.
- Setting `check_stationarity=False` skips the `stationarity_tests()` pre-checks when the caller has already detrended/differenced the series.

