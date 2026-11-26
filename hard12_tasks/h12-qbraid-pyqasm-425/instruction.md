You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Bare expression statements crash with `AttributeError` instead of raising `ValidationError`

## Limitation

An expression followed by a semicolon is a syntactically valid OpenQASM 3 statement — the
[classical types](https://openqasm.com/versions/3.1/language/classical.html) chapter uses this form throughout to
illustrate operator results, for example under
[Integers](https://openqasm.com/versions/3.1/language/classical.html#integers) and
[Angles](https://openqasm.com/versions/3.1/language/classical.html#angles).

`pyqasm` reaches these statements and dereferences `.name` on the expression node. For any
non-`Identifier` expression this raises an `AttributeError` that escapes the public API. The
same dereference fails for an undeclared gate applied to zero qubits.

## Example QASM failure

Straight from the spec's Integers section:

```python
import pyqasm

m = pyqasm.loads('''
OPENQASM 3.0;
int[32] a = 2;
int[32] b = 3;

a * b;   // 6
b / a;   // 1
b % a;   // 1
''')
m.validate()
```

```
AttributeError: 'BinaryExpression' object has no attribute 'name'
```

The spec's Angles section fails identically:

```qasm
OPENQASM 3.0;
angle[4] a = 7 * (pi / 8);
angle[4] b = pi / 8;
a + b;
// AttributeError: 'BinaryExpression' object has no attribute 'name'
```

And the gate-application example in
[Applying gates](https://openqasm.com/versions/3.1/language/gates.html#applying-gates):

```qasm
OPENQASM 3.0;
g1 q1;
// AttributeError: 'str' object has no attribute 'name'
```

## Change Requested

1. Never surface an `AttributeError` from a statement `pyqasm` does not handle. Every
   unhandled statement or expression form must raise `ValidationError` carrying the source
   span.
2. Decide and document the semantics of a bare expression statement. It has no effect on the
   quantum program, so the reasonable options are to evaluate and discard it, or to reject it
   with a clear message such as `"Expression statement has no effect"`. Either is acceptable;
   the current crash is not.
3. An undefined gate identifier must report the undefined name, not fail on an attribute
   lookup.

## Implementation Details

- The root cause is the visitor's dispatch table in `src/pyqasm/visitor.py:193`:

  ```python
  qasm3_ast.ExpressionStatement: lambda x: self._visit_function_call(x.expression),
  ```

  Every expression statement is assumed to be a function call, so `_visit_function_call`
  dereferences `x.expression.name` — which exists on an `Identifier` but not on a
  `BinaryExpression`, a `UnaryExpression`, an `IndexExpression`, or a literal.
- The fix is to branch on the expression type before dispatching: route `FunctionCall` to
  `_visit_function_call` and give every other form the chosen behaviour from point 2 above.
  The generic fallback at `visitor.py:3492` already raises the correct error shape and can be
  reused.
- The `'str' object has no attribute 'name'` variant comes from the gate-operation path, where
  the operation name has already been reduced to a string before the undefined-gate check
  runs. Reorder so the lookup failure is reported first.
- Add a defensive `try/except (AttributeError, TypeError)` around the visitor's top-level
  dispatch that re-raises as `ValidationError` with the statement span. This converts any
  remaining internal slips in the tree into the documented error type — a cheap safety net
  beyond this specific fix.
- Tests: `tests/qasm3/test_validation.py` — assert `ValidationError` (not `AttributeError`)
  for a bare binary expression, a bare function call, a bare identifier, and an undefined gate
  with zero and with one qubit operand.

