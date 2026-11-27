You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] WindowsTransfomer treat_na not working

**Describe the bug**
The darts WindowTransformer does not treat nan values according to its docstring description upon supplying a `treat_na` supported input.

**To Reproduce**

```python
import numpy as np
from darts import TimeSeries
from darts.dataprocessing.transformers import WindowTransformer

values = [0, 1, 2, 3]
series = TimeSeries.from_values(values)

params = {
    "function": "std",
    "mode": "rolling",
    "window": 2,
}

treat_na_inputs = ["dropna", 0.0, "bfill"]
transformers = [WindowTransformer(transforms=params,forecasting_safe=False, treat_na=t) for t in treat_na_inputs]

series_dict = {}
for t,transform in zip(treat_na_inputs,transformers):
    series_dict[f"trea_na input: '{t}'"]=transform.transform(series)

print(series_dict)
```

This yields the output:
```
{"trea_na input: 'dropna'":    rolling_std_2_0
0              NaN
1         0.707107
2         0.707107
3         0.707107

shape: (4, 1, 1), freq: 1, size: 32.00 B, "trea_na input: '0.0'":    rolling_std_2_0
0              NaN
1         0.707107
2         0.707107
3         0.707107

shape: (4, 1, 1), freq: 1, size: 32.00 B, "trea_na input: 'bfill'":    rolling_std_2_0
0              NaN
1         0.707107
2         0.707107
3         0.707107

shape: (4, 1, 1), freq: 1, size: 32.00 B}
```

**Expected behavior**
For `treat_na=`...
* `"dropna"`:  the first entry in the example above should be cut off
* `"bfilling"`:  the first entry should be replaced with the first non-nan one, i.e. 0.707107
* `0.0`:  the first entry should be replaced with `0.0`

**System (please complete the following information):**
 - Python version: [3.12.4]
 - darts version [0.45.0]


