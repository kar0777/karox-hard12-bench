You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Avoid gl_PerVertex redeclarations in WebGL output

## Summary

SPIR-V assembly translated to WebGL can emit a `gl_PerVertex` output-block redeclaration. WebGL ES 3.0 does not support this redeclaration, so glslang rejects the generated artifact even though project translation succeeds.

## Reproduction

```bash
tmp=$(mktemp -d)
cp -R demos/open-source-porting/cases/spirv-tools-basic-src "$tmp/case"
.venv/bin/python -m crosstl._crosstl translate-project "$tmp/case" \
  --output-dir issue-probe-out \
  --report "$tmp/case/issue-probe-out/report.json" \
  --validate \
  --no-format \
  --target webgl
glslangValidator -S vert "$tmp/case/issue-probe-out/webgl/basic_src.webgl.glsl"
```

## Current Result

Generated WebGL begins with:

```glsl
#version 300 es
out gl_PerVertex {
    vec4 gl_Position;
    mediump float gl_PointSize;
    float gl_ClipDistance[8];
    float gl_CullDistance[8];
};
```

`glslangValidator` reports:

```text
'vertex output block' : not supported for this version or the enabled extensions
'built-in block redeclaration' : not supported for this version or the enabled extensions
'gl_Position' : cannot redeclare a non block as a block
```

## Expected Result

WebGL output should assign to builtins such as `gl_Position` without redeclaring `gl_PerVertex`, or emit a structured diagnostic if the source requires unsupported clip/cull distance semantics.

## Acceptance Criteria

- `spirv-tools-basic-src` WebGL output validates with `glslangValidator -S vert`.
- WebGL codegen does not emit `gl_PerVertex` redeclarations for GLSL ES 300 output.
- Add focused coverage for SPIR-V `BuiltIn Position` translation to WebGL.

