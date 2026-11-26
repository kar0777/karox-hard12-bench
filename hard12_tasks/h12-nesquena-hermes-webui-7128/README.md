# HARD12 task `h12-nesquena-hermes-webui-7128`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/7128 |
| issue | #7126 (created 2026-08-18) |
| PR created / merged | 2026-08-18 / 2026-08-19 |
| base | `bec67d60ea86aead59445173f843e7b56911eade` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 2 / 10 |
| test files | tests/test_large_session_fuzzy_duplicate_bound.py, tests/test_merge_append_only_normalization_cache.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
