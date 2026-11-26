You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[BUG] `rebase(BasisSet.CLIFFORD_T)` silently drops `rx`/`ry`/`rz` gates

Hi, we're doing some work on testing quantum circuit transformation tools and came across the following issue while evaluating `PyQASM`:

### Environment

- **PyQASM version**: 1.2.0
- **Python version**: 3.10.12
- **Operating system**: Ubuntu 22.04.5 LTS (WSL2)


### What happened?

`QasmModule.rebase(BasisSet.CLIFFORD_T)` silently removes any `rx`, `ry`, or `rz` gate from the circuit. No exception is raised and no warning is printed, the gate is simply gone from the output, and the circuit's measured output distribution changes as a result. This isn't specific to any one angle: for all angles we tested, including `pi/3`, which has no exact Clifford+T representation.

### How can we reproduce the issue?

```python
from pyqasm import dumps, loads
from pyqasm.elements import BasisSet

qasm = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
creg c[1];
ry(-pi/4) q[0];
measure q[0] -> c[0];
"""

circuit = loads(qasm)
print(dumps(circuit.rebase(BasisSet.CLIFFORD_T, in_place=False)))
```

Output: the `ry(-pi/4) q[0];` line is gone, the `measure` survives untouched. Measuring the input circuit gives `{0: 0.8536, 1: 0.1464}`; measuring this (wrong) output gives `{0: 1.0}` instead.

### What should happen?

The rebase should preserve the circuit semantics, or fail explicitly if the requested operation cannot be represented in the target basis. In this example, `ry(-pi/4)` is exactly representable in Clifford+T; for example, `sdg; h; tdg; h; s` is equivalent up to global phase. The gate should not be silently removed.

### Where does this come from?

In `pyqasm/decomposer.py`, `Decomposer.process_gate_statement` has a branch for `gate_name in {"rx", "ry", "rz"}` whose body is just a comment describing an intended Solovay-Kitaev approximation (`# approx_gates = solovay_kitaev_algo(...)`) followed by `pass`. The function's gate-list accumulator was initialized to `[]` earlier and this branch never populates it, so the gate is dropped. `pyqasm/maps/decomposition_rules.py` has a matching commented-out `solovay_kitaev_algo` stub with a `TODO` above it.

### Suggestions (Optional)

_No response_
