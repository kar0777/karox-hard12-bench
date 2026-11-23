You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Verifier: a value's postcondition/refinement is not propagated through an ADT field (box then unbox loses the fact)

## Summary

A verifier **incompleteness** (not a soundness bug): a value's postcondition or refinement is not propagated **through an ADT field**. When a provably-constrained value is stored into a `data` constructor field and later recovered with `match`, the constraint is forgotten, so a postcondition whose truth depends on that constraint cannot be discharged at Tier 1.

This is conservative — the verifier never *proves* a false property; it only fails to prove some *true* ones (and the contract is still enforced at runtime).

## Reproduction

```vera
private data Box { MkBox(Int) }

private fn mag(@Int -> @Int)
  requires(true) ensures(@Int.result >= 0) effects(pure)   -- mag GUARANTEES result >= 0
{ if @Int.0 < 0 then { 0 - @Int.0 } else { @Int.0 } }

public fn main(@Unit -> @Int)
  requires(true) ensures(@Int.result >= 0) effects(pure)   -- TRUE: the field can only come from mag
{
  let @Box = MkBox(mag(-5));               -- box a provably->=0 value
  match @Box.0 { MkBox(@Int) -> @Int.0 }   -- unbox and return it
}
```

```
$ vera check  main.vera    # OK
$ vera verify main.vera    # Cannot statically verify postcondition in 'main'. Function body
                           # uses constructs outside the decidable fragment. Contract will be
                           # checked at runtime.  ->  3 verified (Tier 1), 2 runtime checks (Tier 3)
$ vera run    main.vera    # 5   (mag(-5) = 5 >= 0 — the Tier-3 runtime check passes)
```

`main`'s postcondition `result >= 0` is genuinely true (the field can only have been produced by `mag`), but the `>= 0` fact attached to `mag`'s result is dropped the moment it is stored into `MkBox`'s field and recovered by `match`. The unboxed value is treated as an arbitrary `Int`, so the obligation cannot be discharged at Tier 1 and **degrades to a Tier-3 runtime check** (on some program shapes it instead surfaces as an unprovable obligation / counterexample rather than a demotion — same underlying gap).

## Why this is a limitation, not a bug

- **Sound**: the verifier never proves a false property. The *false* variant (`ensures(@Int.result > 0)`, which is not always true here) is still correctly rejected, and the contract is enforced at runtime. Full postcondition/refinement propagation through arbitrary data structures is undecidable in general; Vera's verifier degrades gracefully to Tier 3 (DESIGN.md: "degrades gracefully where SMT is undecidable").
- **Not module-specific**: reproduces identically with a same-file callee (`mag` above) and a cross-module callee (a module `magnitude` boxed then unboxed), confirming it is a general ADT-field fact-propagation gap, not a codegen or module-resolution issue.

Same family as the verifier reporting/completeness gaps #764, #776, #779 (statically-obligated-elsewhere or runtime-guarded; the program never does the wrong thing).

## Workarounds

- Give the field a refinement type so the constraint travels with it, or
- re-establish the fact after unboxing (an explicit narrowing / assertion), or
- accept the Tier-3 runtime check, which enforces the contract dynamically.

## Provenance

Surfaced by the adversarial review of PR #907 (observation N2). Pre-existing; the verifier stage is untouched by that PR.

