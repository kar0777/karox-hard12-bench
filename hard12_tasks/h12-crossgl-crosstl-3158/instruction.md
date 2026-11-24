You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

OpenCL C input: barrier(flags) keeps only the work-group memory fence

The OpenCL C importer lowers `barrier(flags)` and `work_group_barrier(flags)` to `workgroupBarrier()` whatever the flags say (`visit_SyncNode` in `crosstl/backend/OpenCL/OpenCLCrossGLCodeGen.py`). `workgroupBarrier()` orders only work-group memory, so `barrier(CLK_GLOBAL_MEM_FENCE)` and `barrier(CLK_IMAGE_MEM_FENCE)` lose their global and image memory ordering and no diagnostic is raised.

For `barrier(CLK_GLOBAL_MEM_FENCE)`, checked on main at 000f59e1:

| Target | Output |
| --- | --- |
| SPIR-V | `OpControlBarrier Workgroup Workgroup` with `AcquireRelease \| WorkgroupMemory` |
| HLSL | `GroupMemoryBarrierWithGroupSync()` |
| Metal | `threadgroup_barrier(mem_flags::mem_threadgroup)` |
| WGSL | `workgroupBarrier()` |

As a result, a kernel that writes a global buffer before the barrier and then reads another work-item's element after it can read stale data on these targets.

The issue comment on #2838 raised this, and #2972 left it alone because it lowers only the fence builtins. The barrier should order the memory its flags name, for example by pairing the execution barrier with the matching CrossGL fence. A flag combination that cannot be kept should raise a typed refusal.

