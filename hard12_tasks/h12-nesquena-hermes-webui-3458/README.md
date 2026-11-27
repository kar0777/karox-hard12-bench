# HARD12 task `h12-nesquena-hermes-webui-3458`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/3458 |
| issue | #3355 (created 2026-06-01) |
| PR created / merged | 2026-06-03 / 2026-06-03 |
| base | `bb5aa02523b335b0eb937c707576df95d30e265f` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 5 / 5 |
| test files | tests/test_agent_health_remote.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
