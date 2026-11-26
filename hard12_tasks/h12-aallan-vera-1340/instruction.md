You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A module generic instantiated from an effect-operation result never registers its clone — caller silently dropped

A generic declared in a module, instantiated at a type that comes from an effect-operation result, never registers its clone: codegen reports a compilation note (`call target 'mod$<module>$<fn>$<T>' not registered`) and silently drops the calling function from the emitted module. The program is check-green and verify-green.

## Repro

```vera
-- mlib5.vera
module mlib5;

private forall<T> fn idg(@T -> @T)
  requires(true)
  ensures(true)
  effects(pure)
{
  @T.0
}

public forall<T> fn outer(@T -> @Int)
  requires(true)
  ensures(true)
  effects(pure)
{
  handle[State<Int>](@Int = 42007) {
    get(@Unit) -> { resume(@Int.0) },
    put(@Int) -> { resume(()) }
  } in {
    idg(get(()))
  }
}
```

Entry: `import mlib5(outer);` and a `main` calling `outer(1)`.

```
$ vera check  → OK
$ vera verify → OK
$ vera run
Compilation notes:
  - Function 'outer$Int' body contains unsupported FnCall: call target 'mod$mlib5$idg$Int' not registered
```

`main` is absent from the emitted module.

## Bisected conditions

Necessary, both: the generic is declared in a **module** (its clone is the `mod$`-mangled form), and its type argument is inferred from an **effect-operation result**. Not needed: nesting under a `where` helper, or the generic being `private` (`public` fails the same way).

Controls that pass: a literal type argument; a type argument from a plain module-function result; the identical shape with the generic declared in the entry file.

## Family

The `mod$`-mangled registration path for module generics — the #1274/#1281 machinery — distinct from #1299's scope-table divergence (whose fix neither causes nor changes this: behavior is identical on `release/v0.1.12`'s base and on the #1299/#1281 branch).

Found by the adversarial review of the #1299/#1281 branch while dispositioning a probe pair whose control shared the trigger. The KNOWN_ISSUES row rides that PR.

