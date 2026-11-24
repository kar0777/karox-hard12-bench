You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] SKLearnModel.fit() misses per-series covariate width mismatches when feature counts cancel

**Describe the bug**

`SKLearnModel.fit()` checks the individual target, past-covariate and future-covariate widths only when the total lagged feature count differs from the first item. Two schema errors can cancel: if the first item has one past and two future components and the second has two past and one future, equal lag counts give the same aggregate width, so `fit()` succeeds on inconsistent inputs. Prediction on the second item then fails.

**To Reproduce**

```python
from darts.models import LinearRegressionModel
from darts.utils.timeseries_generation import linear_timeseries

targets = [linear_timeseries(length=30), linear_timeseries(length=30)]
past = [
    linear_timeseries(length=30),
    linear_timeseries(length=30).stack(linear_timeseries(length=30)),
]
future = [
    linear_timeseries(length=30).stack(linear_timeseries(length=30)),
    linear_timeseries(length=30),
]

model = LinearRegressionModel(
    lags=2,
    lags_past_covariates=2,
    lags_future_covariates=[0, 1],
)

model.fit(targets, past_covariates=past, future_covariates=future)
model.predict(
    1,
    series=targets[1],
    past_covariates=past[1],
    future_covariates=future[1],
)
```

`fit()` succeeds because both items produce eight lagged features, and the model stores `{'target': 1, 'past': 1, 'future': 2}`. `predict()` then rejects the second item, which has `{'target': 1, 'past': 2, 'future': 1}`.

**Expected behavior**

`fit()` should reject the second item before training the estimator, with an error that names index 1 and both the past- and future-covariate mismatches.

Root cause: there is an existing TODO for this case. The per-component width checks are nested inside `if expected_nb_feat != X_i.shape[1]:`, so they never run when the aggregate widths match.

Proposed fix: move the per-input width checks out of that condition so they run for every series item, then keep the aggregate feature-count check after them. This resolves the TODO. With it, the cancelling case raises during `fit()` naming both mismatches at index 1, a valid multi-series control still fits, and the focused SKLearn fit/runnability tests (90) pass.

**System (please complete the following information):**
 - Python version: 3.13
 - darts version: master (ca413d65)

**Additional context**

This intentionally turns an invalid fit that is currently accepted into an early `ValueError`.

