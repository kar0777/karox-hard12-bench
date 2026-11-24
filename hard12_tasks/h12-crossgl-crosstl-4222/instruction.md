You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

A generic struct member of type `vecN<T>` is written `T2` after specialisation

On main at 178f5034, a generic struct with a `vec2<T>` member keeps the type parameter in the member's vector name after specialisation. A scalar `T` member is substituted correctly.

```glsl
shader main {
    struct VBox<T> { vec2<T> v; T s; };
    buffer float* results;
    compute {
    @ numthreads(1, 1, 1)
    void main() {
        VBox<float> b;
        b.v = vec2(1.0, 2.0);
        b.s = 3.0;
        results[0] = b.v.x + b.v.y + b.s;
    }
    }
}
```

```bash
crosstl translate vbox.cgl --backend hip --output vbox.hip
crosstl translate vbox.cgl --backend metal --output vbox.metal
crosstl translate vbox.cgl --backend directx --output vbox.hlsl
```

HIP output declares `struct VBox_float { T2 v; float s; };`, and clang's HIP device syntax check reports `error: unknown type name 'T2'`. Metal output fails the same way (`xcrun metal`: `error: unknown type name 'T2'`), and so does HLSL (DXC 1.9: `error: unknown type name 'T2'`). CUDA and Slang output fail on the struct itself (#4002). With #4187 they specialise it, but still write `T2 v;`.

The member type reaches `generic_struct_specialized_fields` already spelled `T2`, so the string substitution of `T` has nothing to replace. #4184 fixes the same spelling for array parameters of generic functions (#4001), not for struct members.

Expected: `float2 v;` (HIP, CUDA, Metal, HLSL, Slang) and `vec2 v;` (GLSL).

Found while reviewing #4187.

