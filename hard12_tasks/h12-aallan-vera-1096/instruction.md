You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Direct index on a nested type-var-element builtin call is E602-dropped though check and verify pass

A program that passes `vera check` and `vera verify` is refused by codegen when it **directly indexes the result of a nested type-var-element builtin call**. The function is E602-dropped ("could not infer index expression element type") and the module then fails to assemble.

## Repro

```vera
public fn main(-> @Int) requires(true) ensures(true) effects(pure) {
  array_reverse(array_reverse([10, 20, 30]))[0]
}
```

- `vera check` → exit 0, no diagnostics. `vera verify` → exit 0.
- `vera compile` / `vera run` → `[E602] unsupported IndexExpr: could not infer index expression element type — function skipped`, then `unknown func: failed to find name $main`.
- The let-bound form of the identical expression computes correctly (`let @Array<Int> = array_reverse(array_reverse([10, 20, 30])); @Array<Int>.0[0]` → `10`), so the value is well-defined — this is a codegen inference completeness gap, not unsoundness. The drop is loud, never silent-wrong.

## Trigger matrix (controlled A/B)

Broken — `outer(inner(...))[i]` where **outer** is an element-preserving type-var-element builtin (`array_reverse`, `array_sort_by`, `array_flatten`) and **inner** is itself a type-var-element builtin:

- `array_reverse(array_reverse(x))[0]`
- `array_sort_by(array_reverse(x), cmp)[0]`
- `array_reverse(map_values(@M.0))[0]` (with `@M` a `Map<String, Int>` slot)
- `array_sort_by(map_values(@M.0), cmp)[0]`

Works today:

- `array_reverse(array_concat(a, b))[0]` — inner is consultor-resolvable
- `array_map(map_values(@M.0), f)[0]` — outer's element type comes from the closure
- single-level `map_values(@M.0)[0]`, `array_reverse(@A.0)[0]`
- every let-bound form

## Root cause

`_typevar_elem_builtin_ret_named_type` (vera/wasm/inference.py:1665): the class-1 arm resolves its argument via `_named_type_from_arg_info(args[0])`, which is consultor-only and returns `None` for a nested type-var-element inner call. The docstring documents this as harmless — "such nested calls already fail to emit as a call argument upstream, so the enclosing index drops regardless" — but that assumption is no longer true: the nested call emits fine (the let-bound form runs), so the `None` now drops an otherwise-compilable function.

Fix sketch: resolve the argument via `_builtin_call_ret_named_type(args[0])` (which recurses into this helper) instead of the consultor-only lookup, in the class-1 forwarding arm and the class-2 analog.

Found while auditing example candidates for the v0.1.5 docs sweep; the natural spelling of a sort-then-take-top step over an alias-spelled `Map` trips exactly this shape.

