You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A generic instantiated at a function type is accepted by `vera check` and refused by `vera compile`: the judgment is made only at lowering (E622 today; E604 + E620 at the clone once the checker names the instantiation)

## Mechanism

A call that instantiates a generic at a function type, `idg(fn(@Int -> @Int) effects(pure) { @Int.0 * 2 })` for `forall<T> fn idg(@T -> @T)`, passes `vera check` and `vera verify`. Code generation refuses it. On `main` the clone-discovery walker cannot name a closure literal's type, so the call is E622, "Cannot infer a generic call's type argument". With the checker's own instantiation naming the clone (Stage 26, the pull request for #1679, which retires E622), the clone `idg$fn(Int -> Int)` is built and its lowering is refused with E604, "Unsupported state effect type", and E620, "Function dropped: skipped callee or no function table". Either way the judgment that a generic is not instantiated at a function type is made only by code generation, after the checker accepted the program, and the codes it is made with describe something else (a state effect's cell type; a dropped function).

Measured on `main` at 6141d6ad (E622) and on the Stage 26 branch (E604 + E620, `idg$fn_U28_Int_S_U2d__R_SInt_U29_`).

## Reproduction

`mlib.vera`:

```vera
module mlib;

type IntToInt = fn(Int -> Int) effects(pure);

private forall<T> fn idg(@T -> @T)
  requires(true)
  ensures(true)
  effects(pure)
{
  @T.0
}

public fn compute(@Unit -> @Int)
  requires(true)
  ensures(true)
  effects(pure)
{
  let @IntToInt = idg(fn(@Int -> @Int) effects(pure) { @Int.0 * 2 });
  apply_fn(@IntToInt.0, 21)
}
```

`main.vera`:

```vera
import mlib(compute);

public fn main(@Unit -> @Int)
  requires(true)
  ensures(true)
  effects(pure)
{
  compute(())
}
```

`vera check main.vera` and `vera verify main.vera` pass; `vera compile main.vera` exits 1 with E622 at the `idg(...)` line of `mlib.vera` (the two programs `tests/test_uninferred_type_arg_e622.py` holds as `_MODULE_OWNED_SITE` and `_MODULE_OWNED_SHADOWED`).

Expected: one judgment, at check. Either the instantiation is lowerable, so the program compiles and `vera run` prints 42, or the checker refuses it at the call with one code that says a generic cannot be instantiated at a function type, and the limitation tables say so.

## Effect

Loud: a program `vera check` and `vera verify` accept is refused by `vera compile`, with codes that describe another defect.

## Reach

The suite's two programs above, retired with E622 by Stage 26's pull request. A user program meets it when a closure, or a slot of a function type, is passed at a generic's `@T` parameter. Occurrences in the corpus and the docs are not measured.

## Class

A judgment that depends on a generic's instantiation, made only by code generation (#1679). The pull request that closes #1679 moves its listed judgments to the root call and leaves this one; it is tracked here from that merge. The decision is the language's (DESIGN.md, spec chapter 2's generics): a clone at a function-typed argument lowers (closures are values and `apply_fn` calls them), or the checker refuses it with its own code and a limitation row.

Found during Stage 26's test migration (the former E622 cells).

