You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] Missing `ccx` decomposition in `rebase` for `ROTATIONAL_CX` and `CLIFFORD_T`

### Environment

- pyqasm version: 1.3.0 (also `main` at `62b012e`)
- Python version: 3.11.16
- OS: Ubuntu 22.04.5 LTS (WSL2)

### What happened?

`rebase(BasisSet.ROTATIONAL_CX)` and `rebase(BasisSet.CLIFFORD_T)` raise `RebaseError` on a program with a single `ccx`. `validate()` and `unroll()` accept the same program, and the unrolled program still contains the `ccx`.

### How can we reproduce the issue?

```python
import pyqasm
from pyqasm.elements import BasisSet

module = pyqasm.loads("""OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
ccx q[0], q[1], q[2];
""")
module.validate()
module.rebase(BasisSet.ROTATIONAL_CX)
```

Output:
```
pyqasm.exceptions.RebaseError: Gate 'ccx' is not supported in the 'BasisSet.ROTATIONAL_CX set'.
```

The user guide says there is "complete conversion support for the `BasisSet.ROTATIONAL_CX` basis set". When we tried every qelib1 gate on its own, `ROTATIONAL_CX` rejected three of them: `ccx`, `id`, and `c3x` (reported as `Gate 'p' is not supported`). Interestingly, `cswap` can be rebased successfully because it is already expanded into simpler gates, whereas `ccx` remains as a single gate after unrolling.

### What should happen?

`ccx` should be decomposed into both `ROTATIONAL_CX` and `CLIFFORD_T`, while `c3x` should be decomposed into `ROTATIONAL_CX`. The `id` gate can simply be removed in either case.


### Suggestions (Optional)

The issue appears to come from missing decomposition rules in `decomposition_rules.py`. `ccx` is retained by unroll, while `c3x` is expanded into gates including `p`, which is also missing from the target basis and decomposition rules.

One possible fix is to add the missing rules for `ccx`, `id`, and `p`, along with support for selecting a third qubit in the decomposition rules.

We prototyped this approach. The resulting circuits match their original unitaries up to global phase, all 1,011 existing tests pass, and five new regression tests fail before the change and pass afterward.
