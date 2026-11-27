You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Checker types `Int <op> Nat` as `Nat`, inferring spurious @Nat narrowings

Surfaced while implementing #747 (the @Nat binding-site narrowing generalization).

## Finding

A non-negative integer literal is typed `Nat`, and the binary-arithmetic rule promotes the result to `Nat` whenever **either** operand is `Nat` — so an `Int <op> Nat-literal` expression is typed `Nat` even though it can be negative:

```
@Int.0 + 2   ->  Nat
@Int.0 * 2   ->  Nat
@Int.0 - 2   ->  Nat     -- clearly unsound: Int - 2 can be negative
```

(reproduced via `typecheck_with_artifacts` on `fn f(@Int -> @Int) { @Int.0 <op> 2 }`).

## Impact

The `Int - Nat` case is masked downstream by #520's underflow-leaf check and #552's narrowing obligation (a pure-literal subtraction is still obligated `>= 0`), so it does not produce unsound *verified* code today. But the promotion drives **spurious @Nat narrowing inferences** at other sites: an `async(@Int.0 * 2)` infers `Future<Nat>`, so the `@Int -> @Nat` narrowing fires (counterexample `@Int.0 = -1`) on an expression the author never annotated as `Nat`. `tests/conformance/ch09_async.vera` was worked around with an explicit `requires(@Int.0 >= 0)` on its helper rather than letting the inferred `Nat` stand.

## Fix direction

`Int <op> Nat` (and `Nat <op> Int`) should type as `Int` for addition/multiplication/subtraction — the result is only `Nat` when **both** operands carry `Nat` provenance. The non-negative-literal-is-`Nat` rule is fine in isolation; the unsoundness is in the binop promotion. See the numeric-type join logic in `vera/checker/` and `vera/types.py`.
