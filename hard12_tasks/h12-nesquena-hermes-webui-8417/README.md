# HARD12 task `h12-nesquena-hermes-webui-8417`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/8417 |
| issue | #8345 (created 2026-10-17) |
| PR created / merged | 2026-10-20 / 2026-10-20 |
| base | `7c7cedfca5bec55dc423f5eb70eb52470f0dc7b9` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 8 / 79 |
| test files | tests/test_insights.py, tests/test_issue8345_insights_cache_denominator.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
