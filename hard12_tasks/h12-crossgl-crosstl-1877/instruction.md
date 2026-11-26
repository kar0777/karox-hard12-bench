You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Lower partial aggregate value-initialization to valid HLSL

## Problem

Source aggregate value-initialization can reach HLSL as a partial fixed-array initializer such as `float values[4] = {0};`. DXC requires every fixed-array element to be present and reports `too few elements in vector initialization`. Expanding only scalar vector constructors does not cover arrays, nested arrays, structures, or arrays of structures.

## Expected behavior

Lower contextual aggregate initializers to complete HLSL initializers while preserving source value-initialization rules. Omitted trailing members and elements must receive the correct recursive zero/default value; excess or unresolved shapes must produce a structured diagnostic.

## Acceptance criteria

- Expand `{0}` and partially specified fixed arrays to the declared extent in HLSL.
- Recursively value-initialize nested arrays, structures, matrices, vectors, and arrays of structures.
- Preserve source matrix orientation and explicit initializer order.
- Infer the aggregate shape from declarations, assignments, returns, and parameter contexts without duplicating side effects.
- Reject unknown extents, excess elements, and unsupported non-default construction with structured project diagnostics.
- Add DXC coverage for numeric arrays, complex/structure arrays, nested aggregates, and partially initialized returns.
- Keep existing scalar-to-vector splat behavior distinct from fixed-array initialization.

## Real-world impact

At MLX commit `968d264f2903d578e699c4452a4dbf48633921aa`, official DXC `v1.9.2602.24` reports 88 partial-initializer errors while compiling the generated `gemv.metal` DirectX artifact:

```hlsl
float result[4] = {0};
```

```text
error: too few elements in vector initialization (expected 4 elements, have 1)
```

The same artifact also contains eight-element fixed-array cases initialized with only two explicit elements. OpenGL already has recursive aggregate zero-fill coverage that can inform the shared contextual-shape contract, but HLSL output must be validated independently with DXC.

## Related work

- #930 covered scalar Metal vector constructors, not fixed arrays or recursive aggregates.

