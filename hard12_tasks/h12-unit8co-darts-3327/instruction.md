You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] LinearRegression get_estimator method's required arguments appear to do nothing

**Describe the bug**

No matter what is passed into the [get_estimator](https://unit8co.github.io/darts/_modules/darts/models/forecasting/regression_model.html#RegressionModel.get_estimator) method of the LinearRegression class the same model object is returned.

**To Reproduce**

```python
from darts import TimeSeries
from darts.models.forecasting.linear_regression_model import RegressionModel
from darts.utils.timeseries_generation import linear_timeseries

import numpy as np

trend = linear_timeseries(start_value=0, end_value=100, length=100)
noise = TimeSeries.from_times_and_values(
    trend.time_index, np.random.normal(0, 5, size=trend.values().shape)
)

series = trend + noise

model = RegressionModel(lags=3, output_chunk_length=2)
model.fit(series)

print(id(model.get_estimator(1, 1)))
print(id(model.get_estimator(2, 2)))
print(id(model.get_estimator(-1e7, -1e7)))
print(id(model.get_estimator(1e7, 1e7)))
```
```
13699865568
13699865568
13699865568
13699865568
```

**Expected behavior**
My assumption was that a Darts model would build 1 underlying model per future time period, i.e. "direct forecasting". `get_regressor` takes 2 arguments:

```python
    def get_estimator(self, horizon: int, target_dim: int):
        """Returns the estimator that forecasts the `horizon`th step of the `target_dim`th target component.

        The model is returned directly if it supports multi-output natively.

        Parameters
        ----------
        horizon
            The index of the forecasting point within `output_chunk_length`.
        target_dim
            The index of the target component.
        """
```

No matter the arguments passed in the method will...
1) return an object without an error, even if the inputs are ridiculous
2) return the same model object (not sure which horizon's model this is).

Both are unexpected to me.

**System (please complete the following information):**
 - Python version: 3.12
 - darts version: 0.30.0

**Additional context**
New to darts. 

