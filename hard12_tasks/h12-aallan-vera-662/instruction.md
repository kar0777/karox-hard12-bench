You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Layer-1 #626 surfaced 8 silent-skip cases: 7 spurious generic-decl warnings + 1 real codegen gap (head over refinement-of-Array)

## Surfaced by

Layer 1 of [#626](https://github.com/aallan/vera/issues/626) — the new `scripts/check_e602_clean.py` pre-commit gate that fails when any compile emits `[E602]` (body unsupported) or `[E604]` (param unsupported) outside an explicit allowlist.  When the gate first ran across `examples/*.vera` + `tests/conformance/*.vera`, eight functions failed it.  This issue tracks them.

## Two failure shapes

### Shape A — spurious warnings, mono clones work end-to-end (7 functions)

These are generic-decl `[E602]` / `[E604]` warnings that fire against the **template** declaration, while the actual mono clones (produced per call site at `vera/codegen/core.py::compile_program`'s mono-decls loop) compile and run correctly.  Same root cause as the [#604](https://github.com/aallan/vera/issues/604) `option_unwrap_or` / `result_unwrap_or` half — the compilability check is running on the wrong artefact.

| Function | File | Code | Verified-via-mono |
|---|---|---|---|
| `identity` | `examples/generics.vera`, `tests/conformance/ch02_generics.vera` | `E604` | ✓ — `test_generics` returns 42 |
| `const` | `examples/generics.vera` | `E604` | ✓ — `test_generics` returns 42 |
| `is_some` | `examples/generics.vera`, `tests/conformance/ch02_generics.vera` | `E602` | ✓ — `is_some(Some(42))` returns `true` |
| `are_equal` | `tests/conformance/ch09_abilities.vera` | `E604` | ✓ — Eq-constrained generic; ability dispatch in mono clone |
| `cmp_sign` | `tests/conformance/ch09_abilities.vera` | `E604` | ✓ — Ord-constrained generic |

All five are `forall<T>` (or `forall<A, B>`) with bare type-variable parameters.  The mono name-mangler produces e.g. `identity$Int`, `is_some$Int` — those compile cleanly.

### Shape B — real codegen gap, function genuinely missing (1 function)

| Function | File | Code | Trap |
|---|---|---|---|
| `head` | `examples/refinement_types.vera` | `E602` | Calling `head([42, 13, 99])` produces `WAT compilation failed: unknown func: $head` |

`head` is a non-generic function taking a refinement-type-over-Array parameter:

```vera
type NonEmptyArray = { @Array<Int> | array_length(@Array<Int>.0) > 0 };

private fn head(@NonEmptyArray -> @Int)
  requires(true) ensures(true) effects(pure)
{
  @NonEmptyArray.0[0]
}
```

The body `@NonEmptyArray.0[0]` is an `IndexExpr` on a slot whose declared type is `@NonEmptyArray` (a type-alias for a refinement-of-Array).  The translator returns `None` somewhere in this chain — either the IndexExpr translator doesn't unwrap the refinement-alias before checking the element-load shape, or the slot-type resolution stops at the alias name without descending into the refinement's `@Array<Int>` base.

`examples/refinement_types.vera` runs successfully today because `test_refine` doesn't actually call `head` — but a user who copy-pasted `head` and tried to use it would hit the missing-`$head` error.

## Why this isn't [#604](https://github.com/aallan/vera/issues/604)

- **Shape A** is the same root cause as #604's `_unwrap_or` half (warning fires on template; mono works), but the affected functions are user-code, not the prelude.  Fixing #604's diagnostic side ("suppress the warning when at least one mono clone of this generic exists") would close Shape A here as a side effect.
- **Shape B** is a separate codegen gap (refinement-alias-over-Array in parameter position) unrelated to generic monomorphization.  Distinct fix surface.

## Acceptance

- **Shape A**: when #604's diagnostic fix lands, the generic-decl warnings stop firing for both the prelude combinators and the user-code generics here.  The allowlist entries for `identity` / `const` / `is_some` / `are_equal` / `cmp_sign` in `scripts/check_e602_clean.py` can be removed.
- **Shape B**: fix the IndexExpr / slot-resolution chain to handle refinement-alias-over-Array parameters.  Add a regression test exercising `head([1,2,3])` end-to-end.  Remove the `head` allowlist entry.

## Pairs with

- [#604](https://github.com/aallan/vera/issues/604) — same root cause for Shape A.
- [#626](https://github.com/aallan/vera/issues/626) — Layer 1 surfaced these.  Closing this issue (along with #604) is the natural moment to shrink the allowlist in `scripts/check_e602_clean.py` toward empty.
- [#597](https://github.com/aallan/vera/issues/597) — walker-completeness audit; the IndexExpr-on-refinement-alias path is exactly the kind of walker-gap #597 would surface statically.

