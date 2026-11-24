You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Slang input: import cudaThreadIdx, cudaBlockIdx and cudaBlockDim

The Slang importer copies calls to `cudaThreadIdx()`, `cudaBlockIdx()` and `cudaBlockDim()` into CrossGL unchanged, so every generated target then refuses the program with `project.translate.undeclared-function`. Slang declares the three functions in its core module for the CUDA target only (`source/slang/hlsl.meta.slang` at v2026.20, d9ede2dd, lines 27624-27655), where they return CUDA's `threadIdx`, `blockIdx` and `blockDim`. CrossGL already has these values as `gl_LocalInvocationID`, `gl_WorkGroupID` and `gl_WorkGroupSize`.

Reproducer, on `main` at b5118499:

```slang
RWStructuredBuffer<uint> outp;

[shader("compute")]
[numthreads(64, 1, 1)]
void main()
{
    uint3 t = cudaThreadIdx();
    uint3 b = cudaBlockIdx();
    uint3 d = cudaBlockDim();
    uint i = b.x * d.x + t.x;
    outp[i] = i;
}
```

`crosstl.translate("probe.slang", backend="cgl")` keeps the three calls as written. `backend="metal"`, `"vulkan"` and `"directx"` each raise:

```
UndeclaredFunctionError: function 'cudaThreadIdx' is not declared: it is neither a CrossGL built-in function nor a function, structure method, type or callable value of the program (target metal) [project.translate.undeclared-function]
```

Expected: the importer writes `gl_LocalInvocationID`, `gl_WorkGroupID` and `gl_WorkGroupSize` for the three calls.

slangc compiles such a source only with `-target cuda`. #4633 adds the three functions to the Slang coverage rows, checked with nvcc, and Slang input refuses each of them for this reason.

