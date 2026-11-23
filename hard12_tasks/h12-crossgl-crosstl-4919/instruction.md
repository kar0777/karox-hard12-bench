You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Metal and HLSL output copy an unsized array constructor inside a structure's brace list, as in `{float[](1.0, 2.0), 3.0}`

On `main` at 54eed423, an unsized array constructor that is a member of a structure's brace list reaches Metal and HLSL output unchanged:

```glsl
shader Probe {
    buffer float* outp;
    struct W { float m[2]; float s; };
    const W C = {float[](1.0, 2.0), 3.0};
    compute {
        layout(local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
        void main() {
            uint i = gl_GlobalInvocationID.x;
            outp[i] = C.m[1] + C.s;
        }
    }
}
```

- Metal: `constant W C = {float[](1.0, 2.0), 3.0};`. `xcrun -sdk macosx metal -c` fails with `error: expected '(' for function-style cast or type construction`.
- HLSL: `static const W C = __crossgl_construct_W(float[](1.0, 2.0), 3.0);`. `dxc -T cs_6_0 -E CSMain -HV 2021` fails the same way.
- The same list in a local, `W c = {float[](1.0, 2.0), 3.0};`, is copied the same way into Metal output (same error), and HLSL output refuses it with `DirectXAggregateConditionalError: DirectX cannot lower aggregate conditional value 'float[2]' in struct-member-initializer`, which does not describe the construct. SPIR-V output refuses the local with `SPIRVBuiltinLoweringError: Cannot lower call to 'float[]'`.

GLSL and WGSL output compile both. A sized `float[2](1.0, 2.0)` in the same place becomes the list `{1.0, 2.0}` (#3678), and `const float U[] = float[](1.0, 2.0);` takes the element count of its list (#3669), but `array_constructor_shape` in `crosstl/translator/semantics/array_values.py` matches only a literal size, so an unsized constructor is not rewritten.

Expected: the unsized constructor becomes the list of its elements, `{{1.0, 2.0}, 3.0}` on Metal and HLSL, as the sized one does (its member type gives the size), or it is refused with `ArrayConstructorUnsupportedError`.

Found while reviewing #3691.

