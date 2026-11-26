# HARD12 task `h12-nesquena-hermes-webui-7966`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/7966 |
| issue | #7955 (created 2026-10-01) |
| PR created / merged | 2026-10-01 / 2026-10-05 |
| base | `cdff0b8d85a2e3fb789a129facca30bded3bb953` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 19 / 5 |
| test files | tests/test_issue7955_custom_alias_provider_context.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
