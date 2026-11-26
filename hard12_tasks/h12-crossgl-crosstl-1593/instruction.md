You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Disambiguate repeated GLSL interface block names

## Problem

OpenGL generation uses the source struct type name as the GLSL interface block name for every uniform-block instance. When multiple resources share the same struct type, the generated module redeclares the same block name and native compilation fails even though the instance names and bindings are distinct.

Reduced output shape:

```glsl
layout(std140, binding = 0) uniform Params {
    int value;
} first_params;

layout(std140, binding = 1) uniform Params {
    int value;
} second_params;
```

`glslangValidator` reports `Cannot reuse block name within the same interface`.

## Expected behavior

- Assign a deterministic, GLSL-valid interface block name to each distinct uniform-block declaration.
- Preserve the resource instance name, member access remapping, binding allocation, and source type provenance.
- Deduplicate truly identical declarations only when they intentionally describe the same resource.
- Keep names stable across operating systems and project runs.
- Reject conflicting explicit target block-name metadata with a structured diagnostic rather than emitting invalid GLSL.
- Cover repeated struct types across multiple entry parameters and stage scopes with native validator tests.

## Real-world impact

At MLX commit `968d264f2903d578e699c4452a4dbf48633921aa`, OpenGL translation of `mlx/backend/metal/kernels/conv.metal` now lowers runtime-derived global initializers into each compute entry. Native validation advances to repeated `MLXConvParams_2` and `MLXConvParams_3` uniform blocks used by different materialized kernels:

```text
ERROR: 0:300: 'MLXConvParams_2' : Cannot reuse block name within the same interface: uniform
```

This declaration-level fix is useful even before the entry-point-scoped packaging work in #1523, because any valid multi-resource GLSL module may contain multiple instances backed by the same source struct type.

