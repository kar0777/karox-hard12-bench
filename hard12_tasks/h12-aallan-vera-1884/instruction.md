You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

examples/factorial.vera admits every `@Nat` in its contract but traps on overflow from 21

`factorial` in `examples/factorial.vera` declares `requires(true)` and `ensures(@Nat.result >= 1)`, so its contract admits every `@Nat`. But 21! is above u64.MAX, so from 21 on the multiplication overflows and the run traps instead of returning:

```
$ vera run examples/factorial.vera --fn factorial -- 20
2432902008176640000
$ vera run examples/factorial.vera --fn factorial -- 21
Error: Integer overflow
```

`vera verify` reports the multiplication's `int_overflow` obligation `tier3` (line 11, column 5), so the overflow guard is the only evidence for that site, and it fires on inputs the contract admits. The `ensures` is `verified`, because an overflow traps rather than returning a wrong value. The example therefore reads as a function proved for every `@Nat` when it can compute only 0 to 20. `vera test --distrust` (#1634) shows it: 80 of 100 generated inputs trap.

## Fix direction

State the domain the function has: `requires(@Nat.0 <= 20)`. The overflow stays a runtime check, since the verifier cannot bound `factorial(@Nat.0 - 1)` from `ensures(@Nat.result >= 1)`, but no admitted input reaches it. The recursive call's precondition follows from the caller's. The two inputs this example is run on today are inside the domain: `vera run examples/factorial.vera --fn factorial -- 10` in `examples/README.md`, and `test_factorial`'s `factorial(5)`.

Done when `vera test --distrust examples/factorial.vera` passes.

