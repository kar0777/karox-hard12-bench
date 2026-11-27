You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Lower HIP scalar kernel parameters and skip host main in target artifacts

## Summary

After issue #778, the ROCm bit-extract HIP sample now preserves a HIP compute entry in Metal and SPIR-V output, but the generated target artifacts still are not suitable for checked demo validation.

The Metal output emits a scalar kernel parameter without a Metal resource or stage attribute and also emits a host-style `int main()` function. Direct Metal compilation fails. The SPIR-V output validates syntactically, but it still contains an extra fragment `main` entry derived from the host entry point, so the artifact does not cleanly represent only the HIP compute kernel.

## Candidate

- Repository: `https://github.com/ROCm/rocm-examples`
- Commit: `cf369da68f209c315074204bd0eb61d1a5c015d1`
- Source path: `HIP-Basic/bit_extract/main.hip`
- License: MIT

## Reproduction

```toml
[project]
source_roots = ["."]
include = ["main.hip"]
targets = ["cgl", "metal", "vulkan"]
output_dir = "crosstl-out"
```

```bash
python -m crosstl._crosstl translate-project . \
  --output-dir crosstl-out \
  --report crosstl-out/portability-report.json \
  --validate \
  --no-format \
  --target cgl \
  --target metal \
  --target vulkan

python -m crosstl._crosstl validate-project \
  crosstl-out/portability-report.json \
  --format json \
  --run-toolchains

xcrun -sdk macosx metal -c crosstl-out/metal/main.metal -o main.air
spirv-as crosstl-out/vulkan/main.spvasm -o main.spv
spirv-val main.spv
```

## Current Metal output shape

```metal
kernel void bit_extract_kernel(device uint* d_output [[buffer(0)]], const device uint* d_input [[buffer(1)]], uint size) {
}

int main()  {
    return int(0) /* fallback for unmatched generated control flow */;
}
```

`xcrun -sdk macosx metal -c crosstl-out/metal/main.metal -o main.air` reports:

```text
error: invalid type 'uint' (aka 'unsigned int') for input declaration in a kernel function
error: non-qualified function cannot be called 'main'
```

## Current SPIR-V output shape

The SPIR-V artifact contains the expected compute entry point for `bit_extract_kernel`, but also emits:

```text
OpEntryPoint Fragment %26 "main" %29
OpExecutionMode %26 OriginUpperLeft
```

`spirv-as` and `spirv-val` succeed, but the generated artifact still includes a host-entry placeholder as a fragment shader.

## Expected behavior

- HIP host `main` functions should not be emitted as target shader entry points when translating HIP project artifacts.
- HIP scalar kernel parameters should lower to valid target-native input/resource bindings for Metal and SPIR-V, or produce a structured diagnostic if the binding contract cannot be inferred.
- Generated Metal for this candidate should compile with `xcrun -sdk macosx metal -c`.
- Generated SPIR-V for this candidate should contain only the translated HIP compute entry point unless additional shader entries are explicitly present in the source.

This blocks adding the ROCm bit-extract sample to the open-source porting demo with direct Metal compile validation.

