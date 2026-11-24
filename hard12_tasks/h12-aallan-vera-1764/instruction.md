You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

vera test labels a trial's arguments left to right from the first slot, against the De Bruijn order the source uses

## Mechanism

`vera/tester.py::_run_trials` labels a trial's arguments in parameter order, counting each type from 0 left to right, so the first of two `@Nat` parameters is reported as `@Nat.0`. The source names that parameter `@Nat.1`: `@T.0` is the most recent binding of `T` (DE_BRUIJN.md), which is also the order the function's own docstring says the labels follow.

## Effect

Loud: a trial report names the wrong argument whenever two parameters share a type, and its labels contradict the function's own `requires` clause.

## Reach

Every `vera test` trial report, text and `--json`, of a function with two or more parameters of one type.

## Repro (c9235415)

```vera
public fn pair(@Nat, @Nat -> @Int)
  requires(@Nat.1 <= 0 && @Nat.0 >= 5 && @Nat.0 <= 9)
  ensures(true)
  effects(pure)
{
  let @Nat = if @Nat.1 == 0 then {
    -1
  } else {
    @Nat.0
  };
  0
}
```

```text
$ vera test --json --distrust --trials 5 pair.vera
... "args": {"@Nat.0": 0, "@Nat.1": 5} ...
```

The `requires` bounds `@Nat.1`, the first parameter, to 0 and `@Nat.0`, the second, to 5 to 9; the report attaches the names the other way round. The trap the trials hit is #1756's and is independent of the labelling.

