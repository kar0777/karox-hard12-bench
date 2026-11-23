You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

OpenGL and Metal output refuse a 1D shadow texture with an untyped ValueError

OpenGL and Metal output refuse a 1D shadow texture, as HLSL input imports a `Texture1D` or `Texture1DArray` sampled with `SampleCmp*`, with an untyped `ValueError`.

```hlsl
Texture1D<float> shadowLine : register(t0);
Texture1DArray<float> shadowLineArray : register(t1);
SamplerComparisonState compareSampler : register(s0);

float4 main(float coord : TEXCOORD0, float2 coordLayer : TEXCOORD1, float depth : TEXCOORD2) : SV_Target {
    float a = shadowLine.SampleCmp(compareSampler, coord, depth);
    float b = shadowLineArray.SampleCmpLevelZero(compareSampler, coordLayer, depth);
    return float4(a + b);
}
```

With #4421, which fixes the HLSL round trip, `crosstl.translate(path, backend="opengl")` and `backend="metal"` raise:

```text
ValueError: OpenGL texture operation 'textureCompare' requires a declared texture or image resource argument: shadowLine
ValueError: Metal texture operation 'textureCompare' requires a declared texture or image resource argument: shadowLine
```

The same happens when the texture is passed to a helper (`float lookup(Texture1D<float> t, SamplerComparisonState s, float u, float ref)`). HLSL and SPIR-V output translate both programs, and DXC and spirv-val accept them.

Expected: GLSL output declares `sampler1DShadow` and `sampler1DArrayShadow` and writes `texture`, `textureLod` and `textureGrad` with the reference in the coordinate, as GLSL 4.60 section 8.9.2 defines them. Metal has no one-dimensional depth texture, so Metal output refuses the texture with a typed diagnostic that names it.

Found while reviewing #4421.

