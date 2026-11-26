You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Imported function bodies never get the ability-op rewrite — eq/compare in an imported fn fails vera compile with unknown-func (check/verify green)

## Summary

Imported function bodies never receive the Pass-1.6 ability-op canonicalization: `eq(...)`/`compare(...)` in ANY imported function — top-level, direct `where`-helper, or nested helper — stays a raw call that codegen cannot lower, so the body is skipped and `vera compile` on the importing program fails with an internal unknown-func error. `vera check` and `vera verify` are green.

## Reproduction (confirmed at the PR #989 head)

A library whose function body uses `eq`:

```vera
-- lib.vera
public fn iseq(@Int -> @Bool)
  requires(true) ensures(true) effects(pure)
{ eq(@Int.0, 5) }
```

```vera
-- main.vera
import lib(iseq);
public fn main(@Unit -> @Bool)
  requires(true) ensures(true) effects(pure)
{ iseq(5) }
```

`vera check`/`verify` pass; `vera compile main.vera` fails `unknown func: failed to find name $iseq`. The same holds when the `eq` sits in an imported function's direct `where`-helper or a nested helper (three probes: top-level, child, grandchild — all fail identically). Native operators (`==`, `+`) in imported bodies are unaffected.

## Root cause

`_rewrite_ability_ops` (vera/codegen/core.py) rewrites `program.declarations` + monomorphized clones only; Pass 2.5 compiles `self._imported_fn_decls` directly, unrewritten. The same-file path rewrites `eq`/`compare` into `BinaryExpr`/if-chains (recursively through the helper tree since PR #989); the imported path never runs that pass at all.

## Notes

- Pre-existing at base (`3efad78`) — PR #989's recursion fixes did not introduce or change this; its cross-module emission fix uses native operators and is unaffected.
- Same check-green/compile-fail class as the fixed #978 and the open #990: loud failure, no silent miscompile, no false Tier-1.
- Fix direction: run the ability-op rewrite over `_imported_fn_decls` (the full helper tree) before Pass 2.5, sharing the existing recursive `_rewrite_where_fns`.

Found by the PR #989 review round (the FIX-B symmetry probe: does the imported path apply the rewrite the local path applies?).

