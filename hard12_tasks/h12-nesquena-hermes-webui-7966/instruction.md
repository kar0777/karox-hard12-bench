You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

model.provider: ollama makes every Custom-group model fail with custom:<tag-prefix> not configured

With `model.provider: ollama` and a `base_url`, the picker aliases the active provider to `custom`. `model_with_provider_context` then compares the session's `custom` against the raw `ollama`, emits `@custom:qwen3.8:27b`, and `resolve_model_provider` reads `qwen3.8` as a named-provider slug. Reproduced on `dd545190` and still in code on `48186af7`. A local fix returns the bare model when `_resolve_provider_alias(config_provider) == "custom"`.

