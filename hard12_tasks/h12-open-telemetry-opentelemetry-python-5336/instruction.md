You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

opentelemetry-sdk: NaN measurements permanently poison metric aggregations

## Describe your environment

```
OS: Windows 11
Python version: 3.12.7
SDK version: 1.42.1
API version: 1.42.1
```

## What happened?

When a `NaN` value is recorded on a metric instrument (e.g. `counter.add(float("nan"))`), it is silently folded into the running sum and permanently poisons that aggregation. Every subsequent export emits `nan` for that instrument, even if all future measurements are valid.

The root cause: `SumAggregation` guards against negative values with `if amount < 0`, but `float("nan") < 0` evaluates to `False` in Python (all IEEE 754 comparisons against `NaN` return `False`), so `NaN` bypasses the guard and corrupts the running total.

## Steps to Reproduce

```python
import math
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

reader = InMemoryMetricReader()
provider = MeterProvider(metric_readers=[reader])
meter = provider.get_meter("test")

counter = meter.create_counter("test_counter")
counter.add(1)
counter.add(float("nan"))  # poisons the aggregation
counter.add(5)             # valid but sum is now nan

metrics_data = reader.get_metrics_data()
point = (
    metrics_data.resource_metrics[0]
    .scope_metrics[0]
    .metrics[0]
    .data.data_points[0]
)
print(f"sum = {point.value}")           # sum = nan
print(f"is nan = {math.isnan(point.value)}")  # is nan = True
```

## Expected Result

The `NaN` measurement is dropped before aggregation. The counter continues accumulating valid measurements only. Final sum = `6.0`.

## Actual Result

<img width="1292" height="157" alt="Image" src="https://github.com/user-attachments/assets/54a75f17-5704-43f8-92de-3445965070cf" />

```
sum = nan
is nan = True
```

The aggregation is permanently corrupted , all subsequent exports for this instrument emit `nan` with no recovery path.

## Additional context

The Java SDK hit the exact same issue in [open-telemetry/opentelemetry-java#5846](https://github.com/open-telemetry/opentelemetry-java/issues/5846) and resolved it in [PR #5859](https://github.com/open-telemetry/opentelemetry-java/pull/5859) (merged Sep 2023) by explicitly dropping `NaN` measurements at the SDK level before any aggregation occurs.

The proposed fix for Python would be a `math.isnan` / `not math.isfinite` guard early in the `aggregate()` methods. one check per aggregation type, prevents permanent state corruption. Happy to implement this if the direction looks good.

## Would you like to implement a fix?

Yes
