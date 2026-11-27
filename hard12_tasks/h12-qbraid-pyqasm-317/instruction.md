You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] dt duration unit incorrectly mapped to nanoseconds

## Description

The `dt` duration unit in OpenQASM 3 is backend-dependent — it represents the duration of one waveform sample on the target hardware. It cannot be converted to SI units (ns, us, ms, s) without knowing the backend's sample rate.

However, pyqasm currently treats `dt` as equivalent to `ns` during unrolling, producing incorrect duration values.

## Reproduction

```python
from pyqasm import loads
import openqasm3.ast as ast

qasm = """
OPENQASM 3.0;
include "stdgates.inc";
qubit[1] q;
delay[100dt] q[0];
"""

m = loads(qasm)
m.unroll()

for s in m.unrolled_ast.statements:
    if isinstance(s, ast.DelayInstruction):
        print(f"value={s.duration.value}, unit={s.duration.unit.name}")
        # Output: value=100.0, unit=ns
```

## Expected Behavior

`delay[100dt]` should either:
1. Preserve `dt` as the unit in the unrolled AST (`value=100.0, unit=dt`), or
2. Raise an error/warning that `dt` cannot be converted to SI units

## Actual Behavior

The duration is reported as `value=100.0, unit=ns` — treating 1 dt = 1 ns, which is incorrect. The `TIME_UNITS_MAP` in `src/pyqasm/maps/expressions.py` does not include a `dt` entry, so the unit appears to fall through without proper handling.

## Reference

From the [OpenQASM 3 spec](https://openqasm.com/language/delays.html#duration-and-stretch):

> The duration type is used for timing of operations. SI units of time (ns, µs, ms, s) are supported. There is also a backend-dependent unit `dt`, equivalent to the duration of one waveform sample on the backend.
