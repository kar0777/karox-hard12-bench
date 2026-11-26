You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

`end;` statement is unsupported

## Limitation

The [classical instructions](https://openqasm.com/versions/3.1/language/classical.html) chapter defines: "The statement
`end;` immediately terminates the program, no matter what scope it appears in."

`pyqasm` has no handler for `openqasm3.ast.EndStatement` and falls through to the generic
unsupported-statement error.

## Example QASM failure

```qasm
OPENQASM 3.0;
include "stdgates.inc";
qubit[1] q;
h q[0];
end;
```

```
ValidationError: Unsupported statement of type <class 'openqasm3.ast.EndStatement'>
```

Inside a branch, which is the form that carries real meaning:

```qasm
OPENQASM 3.0;
int[8] i = 0;
if (i == 0) { end; }
// ValidationError: Unsupported statement of type <class 'openqasm3.ast.EndStatement'>
```

## Change Requested

1. Accept `end;` wherever a statement is allowed — global scope, loop bodies, `if`/`else`
   blocks, `switch` cases, `box` bodies, and subroutine bodies.
2. At global scope, stop visiting subsequent statements: everything after `end;` is
   unreachable and must not appear in the unrolled output.
3. Preserve `end;` through `dumps()`.
4. Inside a conditional block whose condition depends on a runtime value, `end;` cannot be
   resolved at analysis time. Emit it into the unrolled output as-is rather than attempting to
   truncate the program.

## Implementation Details

- Add an `EndStatement` branch to the statement dispatch in `src/pyqasm/visitor.py`; the
  current fallback that raises is at `visitor.py:3492`.
- The unconditional global-scope case is the simple one: set a flag and stop consuming
  statements at that level.
- Consider whether `QasmModule` should expose that the program contains a terminating `end;` —
  it is the kind of fact the existing `has_measurements()` / `has_barriers()` helpers report,
  and downstream consumers may want it.
- Sanity-check the depth and qubit-count bookkeeping: statements after a global `end;` must
  not contribute, since they are unreachable.
- Tests: `tests/qasm3/test_statements.py` — `end;` at global scope with trailing statements
  that must be dropped, `end;` inside `if`, inside a `for` body, inside a subroutine, and a
  `dumps()` round-trip.

