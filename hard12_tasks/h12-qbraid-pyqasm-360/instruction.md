You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

has_measurements/has_barriers miss loop and switch bodies before unroll()

## Description

`has_measurements()`, `remove_measurements()`, `has_barriers()` and `remove_barriers()` fall back to `self._statements` when the module has not been unrolled. That list can still contain `for` / `while` / `switch` bodies, and the statement walker does not descend into them — so an occurrence inside a loop or switch is invisible.

## Reproduction

```python
from pyqasm import loads

src = """OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
for int i in [0:1] { c[i] = measure q[i]; barrier q; }
"""

m = loads(src)
print(m.has_measurements(), m.has_barriers())   # False False  <- wrong
m.remove_measurements()                          # no-op

m2 = loads(src)
m2.unroll()
print(m2.has_measurements(), m2.has_barriers())  # True True
```

## Scope

Pre-existing — `main` behaves identically, and #345 strictly improves matters by closing the same gap for `box` and `if` on the unrolled path. Filed because #345's walker is the natural home for the remainder, and it would be easy to read that PR as having closed the class of bug entirely.

Note this only affects the **non-unrolled** path. `for`, `while` and `switch` are fully unrolled by `unroll()` and do not reach `_unrolled_ast` with their bodies intact, so `Box` and `BranchingStatement` really are the only two containers the unrolled walk has to handle.

## Suggested fix

Either extend `iter_quantum_statements` to descend into loop and switch bodies for the non-unrolled path, or document on those four methods that they are only meaningful after `unroll()`.

Found in review of #345 (L3).

