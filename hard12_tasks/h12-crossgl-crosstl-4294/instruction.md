You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

SPIR-V, HLSL and GLSL output drop @offset on members of a struct nested in a constant buffer

A member `@offset` (or `@align`) inside a struct that is used as a member of a constant buffer is lost on SPIR-V, HLSL and GLSL output. Each target places the nested member at its natural layout offset, so the shader reads other bytes than the host wrote, and the validators still pass.

Reproducer (`nested.cgl`):

```
shader Probe {
    struct Inner { float s; vec4 v @offset(32); };
    cbuffer C { Inner n; };
    compute {
        layout(local_size_x = 1, local_size_y = 1, local_size_z = 1) in;
        buffer float* outp;
        void main() {
            uint i = gl_GlobalInvocationID.x;
            outp[i] = n.s + n.v.y;
        }
    }
}
```

Observed at ba41e50d9:

| Target | Output for `Inner.v` |
|---|---|
| vulkan | `OpMemberDecorate %Inner_std140_9 1 Offset 16` |
| directx | `float4 v : offset;` (the attribute is emitted as a semantic named `offset`) |
| opengl | `vec4 v;` |
| metal | `float4 v [[offset]];` (not valid MSL) |
| slang | `float4 v : offset;` |

Expected: each target either places `v` at byte 32 of `Inner` or raises a typed `MemberPlacementError`. SPIR-V can write `Offset 32` on the nested struct type. GLSL `layout(offset)` and HLSL `packoffset` do not reach members of a nested struct, so those targets need explicit padding members or a refusal.

Top-level members (`cbuffer C { float s; vec4 v @offset(32); }`) are planned or refused by the new `crosstl/translator/semantics/member_placements.py` (PR for #4196); nested structs need the same treatment.

