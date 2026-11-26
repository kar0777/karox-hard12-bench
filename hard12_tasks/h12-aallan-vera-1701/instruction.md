You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A `match` whose scrutinee is already an error is also reported non-exhaustive (`E313`)

`_check_exhaustiveness` (`vera/checker/control.py`) judges a `match` by the type of its scrutinee.  A scrutinee that is itself an error is typed `Unknown`, which is neither a data type nor `Bool`, so it reaches the infinite-domain arm, and the `match` is also reported `E313`, "Non-exhaustive match: type has infinite domain", however completely its arms cover the type the scrutinee was written to have.  The program is already refused at the scrutinee; the second error is a consequence of the first, and it points at arms that are not wrong.

Measured on `main` at 290c53ab, in the body of `f(@Int -> @Int)`:

| Scrutinee | Arms | Diagnostics |
|---|---|---|
| `@Option<Int>.0`, with no `Option<Int>` binding in scope | `Some(@Int)`, `None` | `E130` at the reference, then `E313` at the `match` |
| `nope(@Int.0)`, a function nothing declares | `Some(@Int)`, `None` | `E200` at the call, then `E313` |
| `@Bool.0`, with no `Bool` binding in scope | `true`, `false` | `E130`, then `E313` |

## Reproduction

```vera
public fn f(@Int -> @Int)
  requires(true)
  ensures(true)
  effects(pure)
{
  match @Option<Int>.0 {
    Some(@Int) -> @Int.0,
    None -> 0
  }
}
```

`vera check` reports `E130` at `@Option<Int>.0`, and `E313` at the `match`, whose arms cover both of `Option`'s constructors.

## Class

Every `match` whose scrutinee's own error leaves it typed `Unknown`: an unresolved slot reference or call, and the result reference that the fix for #1517 refuses with `E163`, which types as `Unknown` as well, so `ensures(match @Tuple<String, Int>.result { Tuple(@Int, @String) -> @Int.0 == @Int.1 })` on a function returning `@Tuple<Int, String>` is reported `E163` and then `E313`.

## Fix direction

`_check_exhaustiveness` does not judge a scrutinee typed `Unknown`, for which an error has already been reported.  A match over any other type is judged as before.

