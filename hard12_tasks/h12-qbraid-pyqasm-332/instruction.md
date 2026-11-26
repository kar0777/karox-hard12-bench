You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

remove_idle_qubits() KeyError: unroll() emits aliased operand nodes that _remap_qubits mutates repeatedly

## Summary

`QasmModule.remove_idle_qubits()` raises `KeyError` on any program whose unrolled AST contains **aliased operand nodes** — the same `IndexedIdentifier` object reused across multiple statements — whenever removing an idle qubit shifts the indices of the qubits those statements use. The minimal trigger is a single `crz` with an idle lower-indexed qubit.

Found while testing the statevector simulator work in #316, but the bug is in `modules/base.py` and pre-dates that branch (reproduces on `main` / released 1.0.3).

## Reproduction

```python
from pyqasm import loads

m = loads('''OPENQASM 3;
include "stdgates.inc";
qubit[3] q;
crz(0.5) q[1], q[2];
''')
m.unroll()
m.remove_idle_qubits()   # KeyError: 0
```

```
File "src/pyqasm/modules/base.py", line 387, in _remap_qubits
    bit.indices[0][0].value = idx_map[old_idx]
KeyError: 0
```

## Root cause

`unroll()`'s decomposition of `crz` emits gate statements whose qubit operands are **the same `IndexedIdentifier` object**, not copies. For the program above, one `q[2]` node is shared by 11 statements and the `cx` operand pair is shared by both `cx` gates:

```python
from collections import Counter
gates = [s for s in m._unrolled_ast.statements if type(s).__name__ == "QuantumGate"]
Counter(id(q) for s in gates for q in s.qubits).most_common(2)
# [(<id>, 12), (<id>, 2)]   <- one operand object reused 12 times
```

`_remap_qubits` (base.py:380-387) then walks every statement and rewrites `bit.indices[0][0].value` **in place**. A node shared by k statements is remapped k times: with `idx_map = {1: 0, 2: 1}` the shared `q[2]` operand goes `2 -> 1` on the first visit, `1 -> 0` on the second, and the third visit looks up `idx_map[0]` -> `KeyError: 0`.

When the remap happens to be the identity (no lower-indexed idle qubit), the repeated remapping is silently harmless, which is why the bug stayed hidden.

## Notes

- Any decomposition that reuses operand nodes triggers this; `crz` is just the minimal known case (`cx`, `swap`, `ccx` unroll with fresh nodes and are unaffected).
- Two possible fixes, not mutually exclusive:
  1. `unroll()` should emit deep-copied operand nodes (aliasing in an AST that later gets mutated in place is a footgun beyond this one crash);
  2. `_remap_qubits` should be idempotent per node, e.g. track visited node ids or rebuild operands instead of mutating shared ones.
- Also affects the `Simulator.run(str)` convenience path in #316, which calls `remove_idle_qubits()` internally.

🤖 Filed with [Claude Code](https://claude.com/claude-code)

