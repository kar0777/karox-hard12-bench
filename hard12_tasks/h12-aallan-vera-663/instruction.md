You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Cross-module imports don't propagate _fn_ret_type_exprs (#614 / #602 cross-module gap)

**Origin:** Surfaced during the code review of [#627](https://github.com/aallan/vera/pull/627) (closing #602).  Same gap exists in #614's already-shipped fix; this issue tracks closing both.

## Problem

The `_fn_ret_type_exprs` registry on `CodeGenerator` (added in PR #625 for #614, re-used in PR #627 for #602) stores each user-declared FnDecl's full Vera return-type expression.  It's populated by `_register_fn` in `vera/codegen/registration.py:44`.  But for **cross-module imports**, the registry is never populated — `vera/codegen/modules.py:60-91` harvests `_fn_sigs` from the imported temp generator via `setdefault`, but doesn't propagate `_fn_ret_type_exprs`.

So a `String`- or `Array<T>`-returning fn defined in module A and called from module B's interpolation (or indexed FnCall, in the #614 case) hits `_fn_ret_type_exprs.get(call.name) → None` and falls through to the silent-skip path that #602 / #614 fixed for in-module calls.

## Concrete failure shapes

### Shape 1 (#602 across modules)

```vera
-- module a.vera
public fn make_str(@Unit -> @String)
  requires(true) ensures(true) effects(pure)
{ "hello" }

-- module main.vera
import a;

public fn main(@Unit -> @Unit)
  requires(true) ensures(true) effects(<IO>)
{
  IO.print("\(make_str(()))\n")  -- still silently wraps with to_string!
}
```

### Shape 2 (#614 across modules)

```vera
-- module a.vera
public fn make_arr(@Unit -> @Array<Int>)
  requires(true) ensures(true) effects(pure)
{ [1, 2, 3] }

-- module main.vera
import a;

public fn main(@Unit -> @Int)
  requires(true) ensures(true) effects(pure)
{
  make_arr(())[0]  -- IndexExpr-of-FnCall element-type inference still fails
}
```

Both shapes will produce the same failure modes as the in-module bugs: WASM validation trap inside a closure, or `[E602]` skip + missing main at top level.

## Fix sketch

In `vera/codegen/modules.py`, alongside the `_fn_sigs.setdefault` harvest, also harvest the imported temp generator's `_fn_ret_type_exprs`:

```python
for fn_name, ret_te in tmp_gen._fn_ret_type_exprs.items():
    self._fn_ret_type_exprs.setdefault(fn_name, ret_te)
```

(Or the equivalent in whatever loop currently does the cross-module harvest.)

## Regression tests needed

Add cross-module variants to:

- `tests/test_codegen_modules.py` — should grow the two shapes above.
- `tests/test_codegen_closures.py::TestIndexExprOfFnCall614` — the closure case for shape 2 across modules.
- `tests/test_codegen.py::TestStringInterpolation` — the interpolation case for shape 1 across modules.

## Why this wasn't caught yesterday

PR #625 (#614 fix) tested in-module shapes only.  The cross-module gap was inherited from `_fn_sigs`'s own cross-module harvest, which has worked fine because it only carries WAT type info (sufficient for call-validation).  The new `_fn_ret_type_exprs` carries richer info that's used by inference; the harvest pattern needs to be extended.

## Pairs with #626

This is one specific instance of the broader "translate returns None → silent skip" pattern tracked by [#626](https://github.com/aallan/vera/issues/626).  Closing #626's Layer 1 (pre-commit gate on `[E602]` warnings on conformance / example programs) might catch this *if* a cross-module example exists in the test corpus — currently doesn't, so independently filing this issue.

