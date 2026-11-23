You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

OpenCL C input refusals are reported as HIP constructs with the hip-import-unsupported code

OpenCL C input reports the constructs that the shared HIP converter refuses as HIP constructs. `OpenCLToCrossGLConverter` inherits `IMPORT_REFUSAL_TYPE = HipImportRefused` from `HipToCrossGLConverter`, and `crosstl/backend/import_refusals.py` has no OpenCL C subclass. So the message, the diagnostic code and `missing_capabilities` all name HIP. (OpenCL-specific refusals such as `project.translate.opencl-atomic-order-unsupported` are not affected.)

```c
__kernel void probe(__global int* outp) {
    int v = 1;
    __asm__ volatile("" : "+r"(v));
    outp[0] = v;
}
```

On main at 1ebda13cf, `python -m crosstl translate probe.cl --backend cgl --output /dev/null` exits 1 with:

```text
Error: CrossGL cannot represent 1 HIP construct: HIP inline asm volatile(""): CrossGL has no inline assembly (target cgl) [project.translate.hip-import-unsupported]
```

From Python, `crosstl.translate("probe.cl", backend="cgl")` raises `crosstl.backend.import_refusals.HipImportRefused`, with `source_name == "hip"`, `missing_capabilities == ("hip.import",)` and `code == "project.translate.hip-import-unsupported"`.

Expected: an `OpenCLImportRefused` (source `opencl`, label `OpenCL C`, its own code), raised by the OpenCL C importer, and reasons that name OpenCL C. The other importers each have their own subclass (`CudaImportRefused`, `HipImportRefused`, `MetalImportRefused`, `SlangImportRefused` and so on).

Project reports carry the same labels. `python -m crosstl translate-project src --target metal --output-dir out --report report.json` on a directory holding only `probe.cl` records one error diagnostic with code `project.translate.hip-import-unsupported` and `missingCapabilities: ["hip.import"]`.

Many reason strings in the shared HIP converter start with `HIP` (`HIP inline asm`, `HIP {form} {target}: CrossGL has no device heap`, `HIP load cache intrinsic ...`). Only some of them can be reached from OpenCL C, so an OpenCL C file can still show HIP wording until those strings take the source label from the converter.

Related: #3295 (OpenCL C input writes `hip_array_extent_4_mul_2`, another HIP name that leaks through the shared converter) and #4387 (importer parse error locations for HIP and OpenCL C).

