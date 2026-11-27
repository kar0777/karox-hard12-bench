# HARD12 task `h12-nesquena-hermes-webui-4559`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/4559 |
| issue | #3928 (created 2026-06-10) |
| PR created / merged | 2026-06-20 / 2026-06-20 |
| base | `d053b29308e47faf0ddac8719a97a0c2ae6c6856` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 7 / 13 |
| test files | tests/test_issue1699_model_cache_source_fingerprint.py, tests/test_issue3928_models_budget_fallback.py, tests/test_model_cache_metadata.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
