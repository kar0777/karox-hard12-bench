You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

consolidate_qubits=True raises AttributeError on gates applied to physical qubits

## Summary

`unroll(consolidate_qubits=True)` raises `AttributeError: 'str' object has no attribute 'name'` for any gate applied to a physical qubit (`$n`). Measurement, reset and barrier on physical qubits are unaffected — they pass the operand through unchanged — so only gates crash.

Found while working on #340: verbatim programs address physical qubits by definition, so they hit this on any consolidating unroll. It is not pragma-specific; the repro below is plain QASM on `main`.

## Repro (pyqasm 1.0.4)

```python
import pyqasm

qasm = """OPENQASM 3.0;
include "stdgates.inc";
h $1;
cz $2, $1;
"""
pyqasm.loads(qasm, device_qubits=5).unroll(consolidate_qubits=True)
```

```
File "src/pyqasm/transformer.py", line 571, in consolidate_qubit_registers
    qubit.name.name,
AttributeError: 'str' object has no attribute 'name'
```

For contrast, these all succeed and keep the physical qubit as written:

```python
pyqasm.loads('OPENQASM 3.0;\nbit c;\nc = measure $2;\n', device_qubits=5).unroll(consolidate_qubits=True)
# c[0] = measure $2;
pyqasm.loads('OPENQASM 3.0;\nreset $1;\n', device_qubits=5).unroll(consolidate_qubits=True)
# reset $1;
```

## Root cause

`Qasm3Transformer.consolidate_qubit_registers` assumes every gate operand is an `IndexedIdentifier` and reads `qubit.name.name` / `qubit.indices[0][0].value`. A physical qubit survives unrolling as `Identifier(name="$1")`, whose `.name` is a plain `str`.

## Expected

Physical qubits are absolute hardware indices; they do not belong to a declared register and there is nothing to consolidate. Gate operands should be left as-is, matching how `measure` / `reset` / `barrier` already treat them (cf. #325).

