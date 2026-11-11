You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

An if or match join of an Int branch with a Nat branch is typed Nat, so the verifier records no narrowing and a verified program traps

## Mechanism

The checker types an `if` whose one branch is a negated literal or literal arithmetic (`-1`, `-1 * -3`) and whose other branch is a `@Nat` as `@Nat`, whatever the literal branch's value. The verifier reads that type and records no `nat_bind` obligation where the value is bound into a `@Nat` `let` or passed to a `@Nat` parameter, while code generation's static rule reads the `UnaryExpr` as `@Int` and plants the guard (`wasm/operators.py:_emit_nat_bind_guard`). The literal on its own (`let @Nat = -1;`), `0 - 1`, the branches swapped, the same join in a `match`, and the join at a `@Nat` return are each obligated and refused with E503.

## Effect

Silent at `vera verify`: a program whose literal branch is `-1` verifies clean, with no `nat_bind` obligation, and `vera run` traps at the guard (`Negative value bound into a @Nat slot`), so no wrong value escapes. With a literal branch whose value is non-negative (`-1 * -3`) the guard never fires, and `vera verify --reconcile` reports it as a check with no record (W004, `guarded_unrecorded`).

## Reach

Found by the program generator (PR #1755), seed 463 of its first 1,000: about one generated program in a thousand. None measured in the corpus, the examples or the docs' Vera blocks. The hand-written shape is a `-1` sentinel branch beside a `@Nat` in a `@Nat` position.

## Repro (c9235415)

```vera
public fn sentinel(@Bool, @Nat -> @Int)
  requires(true)
  ensures(true)
  effects(pure)
{
  let @Nat = if @Bool.0 then {
    -1
  } else {
    @Nat.0
  };
  0
}

public fn through_a_call(@Bool, @Nat -> @Nat)
  requires(true)
  ensures(true)
  effects(pure)
{
  keep(if @Bool.0 then {
    -1
  } else {
    @Nat.0
  })
}

private fn keep(@Nat -> @Nat)
  requires(true)
  ensures(true)
  effects(pure)
{
  @Nat.0
}

public fn tripled(@Bool, @Nat -> @Int)
  requires(true)
  ensures(true)
  effects(pure)
{
  let @Nat = if @Bool.0 then {
    -1 * -3
  } else {
    @Nat.0
  };
  0
}

public fn swapped(@Bool, @Nat -> @Int)
  requires(true)
  ensures(true)
  effects(pure)
{
  let @Nat = if @Bool.0 then {
    @Nat.0
  } else {
    -1
  };
  0
}
```

Expected: `vera verify` refuses `sentinel` and `through_a_call` with E503, as it refuses `swapped`.

Actual:

```text
$ vera verify --json find.vera      # one diagnostic: E503 at line 76, in 'swapped'; 11 verified, 0 Tier 3
$ vera run find.vera --fn sentinel -- true 3        # traps: Negative value bound into a @Nat slot (exit 1)
$ vera run find.vera --fn through_a_call -- true 3  # traps the same way (exit 1)
$ vera run find.vera --fn tripled -- true 3         # 0
$ vera verify --reconcile --json find.vera          # W004 guarded_unrecorded nat_bind at lines 30, 43 and 63
```

