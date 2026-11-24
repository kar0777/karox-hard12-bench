You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

nanoseconds_to_str() drops a microsecond through float rounding (2.3 s prints as 0:00:02.299999)

### pipecat version

`main` (1.14.1.dev)

### Description

`pipecat.utils.time.nanoseconds_to_str()` converts the nanosecond count to float seconds and then pulls the microseconds back out with `(total_seconds - int(total_seconds)) * 1_000_000`. Floating-point error makes that truncate down by one microsecond for many ordinary values, so the formatted string is wrong. This is what `Frame.__str__` uses to print a frame's `pts`, so logs and observers show slightly wrong timestamps.

### Reproduction

```python
from pipecat.utils.time import nanoseconds_to_str

print(nanoseconds_to_str(2_300_000_000))      # 0:00:02.299999  (expected 0:00:02.300000)
print(nanoseconds_to_str(1_000_001_000))      # 0:00:01.000000  (expected 0:00:01.000001)
print(nanoseconds_to_str(3_600_000_001_000))  # 1:00:00.000000  (expected 1:00:00.000001)
```

### Expected

The hours/minutes/seconds/microseconds split should be done with integer arithmetic on the nanosecond value, so exact values print exactly (sub-microsecond digits still truncated, as today).

I have a fix with tests ready and will open a PR.

