You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

BaseSorting.select_periods() drops properties, annotations and the registered recording

[`select_sorting_periods`](https://github.com/SpikeInterface/spikeinterface/blob/9ef464e66c1a36046f7e9ea04c7299fff429c391/src/spikeinterface/core/sorting_tools.py#L558-L562) overwrites `sorting` with the new object, then copies the metadata from this object onto itself:

```python
sorting = NumpySorting(
    sliced_spike_vector, sampling_frequency=sorting.sampling_frequency, unit_ids=sorting.unit_ids
)
sorting.copy_metadata(sorting)
return sorting
```

So after `select_periods`, all properties and annotations are lost. The recording is also no longer registered, so `get_unit_spike_train(..., return_times=True)` ignores the start time or time vector of the recording.

### Reproduction

main at 9ef464e66, Linux (WSL Ubuntu 24.04), Python 3.12.3, numpy 2.5.4:

```python
import numpy as np
import spikeinterface.core as sc
from spikeinterface.core.base import unit_period_dtype

fs = 1000.0
rec = sc.generate_recording(num_channels=2, sampling_frequency=fs, durations=[10.0], seed=0)
rec.shift_times(500.0)  # the recording starts at t = 500 s
sorting = sc.NumpySorting.from_unit_dict(
    {"a": np.array([10, 2000, 5000]), "b": np.array([30, 3000])}, sampling_frequency=fs
)
sorting.set_property("quality", np.array(["good", "mua"]))
sorting.annotate(probe_name="NP2.0")
sorting.register_recording(rec)

periods = np.array([(0, 0, 4000, 0), (0, 0, 4000, 1)], dtype=unit_period_dtype)
selected = sorting.select_periods(periods)

print("properties:   ", sorting.get_property_keys(), "->", selected.get_property_keys())
print("annotations:  ", sorting.get_annotation_keys(), "->", selected.get_annotation_keys())
print("has_recording:", sorting.has_recording(), "->", selected.has_recording())
print("spike times of 'a' (s):", sorting.get_unit_spike_train("a", return_times=True)[:2],
      "->", selected.get_unit_spike_train("a", return_times=True))
```

```
properties:    ['quality'] -> []
annotations:   ['probe_name'] -> []
has_recording: True -> False
spike times of 'a' (s): [500.01 502.  ] -> [0.01 2.  ]
```

The spike times are off by 500 s.

### Possible fix

```diff
-        sorting = NumpySorting(
+        new_sorting = NumpySorting(
             sliced_spike_vector, sampling_frequency=sorting.sampling_frequency, unit_ids=sorting.unit_ids
         )
-        sorting.copy_metadata(sorting)
-        return sorting
+        sorting.copy_metadata(new_sorting)
+        if sorting.has_recording():
+            new_sorting.register_recording(sorting._recording)
+        return new_sorting
```

With this, the properties, annotations and spike times are preserved in the example above. `test_basesorting.py`, `test_baserecording.py`, `test_binaryfolder.py`, `test_binaryrecordingextractor.py` and `test_numpy_extractors.py` still pass (33 tests).

I found no existing report, and no open PR changes this line. It comes from #4316. #4796 fixed a similar loss of start times in `NumpySorting.from_sorting`. I can open a PR with this change and a test.

