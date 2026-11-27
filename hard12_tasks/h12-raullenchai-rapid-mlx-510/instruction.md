You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

frequency_penalty silently no-op on chat completions (penalty has zero observable effect)

## Summary
Setting `frequency_penalty: 2.0` (the OpenAI max) has zero observable effect on output diversity. A prompt designed to elicit repetition emits the same token 10× verbatim even at max penalty.

## Repro
```bash
curl -X POST http://127.0.0.1:8501/v1/chat/completions \
  -H "Authorization: Bearer SEKRET" -H "Content-Type: application/json" \
  -d '{"model":"unsloth/Qwen3.6-27B-MLX-8bit","messages":[{"role":"user","content":"Say the word banana ten times, separated by spaces."}],"frequency_penalty":2.0,"max_tokens":40}'
```
Returns `"banana banana banana banana banana banana banana banana banana banana"` regardless of penalty value. Same output at `frequency_penalty: 0` vs `2.0`.

`presence_penalty` is accepted without error but its effect was not directly tested.

## Severity
**MED** — same "param declared but not wired" family as #459/#464/#465/#468/#469. Field IS declared on `ChatCompletionRequest` (since otherwise Pydantic would 422), but the sampler doesn't apply it. Silently degrades diversity-control workflows.

## Likely scope
Check `vllm_mlx/sampling/`: penalties may be parsed into the SamplerParams object but not actually applied during token sampling. Need to verify whether `mlx-lm`'s sampler supports frequency/presence penalties at all — if not, document the gap and either reject with 400 OR add a custom sampling pass.

Surfaced by iter15 onboarding sweep (hybrid agent).
