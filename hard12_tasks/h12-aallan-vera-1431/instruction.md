You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

E699 Z3 sort mismatch verifying a module that rebuilds an imported Option<Nat> as Option<{refined}>

## Summary

`vera verify` dies with an internal-compiler-error envelope (`[E699] ... Z3Exception: sort mismatch`) on a program `vera check` accepts, when a module matches an **imported** `Option<Nat>` and rebuilds it as an `Option<{refined Int}>`.

Same family as #1360 (a nested `Tuple` inside a constructor) and #884 (`Nat` and `Int` becoming injective sorts): two sorts for one constructor derived by different routes, disagreeing at a datatype position. Here the second type argument is a REFINEMENT rather than a nested `Tuple`, and the two modules are what puts the two derivations apart.

## Repro

`cb.vera`:

```vera
public fn mk(@Int -> @Option<Nat>)
  requires(true)
  ensures(true)
  effects(pure)
{
  int_to_nat(handle[Exn<Int>] {
    throw(@Nat) -> { nat_to_int(@Nat.0) }
  } in {
    throw(@Int.0)
  })
}
```

`ca.vera`:

```vera
import cb;

type Pos = { @Int | @Int.0 > 0 };

public fn relay(@Int -> @Option<Pos>)
  requires(true)
  ensures(true)
  effects(pure)
{
  match cb::mk(@Int.0) {
    Some(@Nat) -> Some(nat_to_int(@Nat.0)),
    None -> None
  }
}
```

`vera check ca.vera` → `OK`. `vera verify ca.vera` → `[E699] ... Z3Exception: sort mismatch`.

## Pre-existence

Reproduced identically at `release/v0.2.0` tip `f23db8f7` — this is not introduced by the guard-completeness work (#1412), which is where it surfaced. It was found while looking for a cross-module narrowing site that remains unguarded after #757 closed the generic-instantiated constructor field.

## Note on the envelope

`verify --json` does emit a parseable `E699` envelope here, so #1360's second half (the machine-readable contract holding through a translator bug) is working. What is missing is the sort agreement itself.

