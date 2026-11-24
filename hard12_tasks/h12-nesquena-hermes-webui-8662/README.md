# HARD12 task `h12-nesquena-hermes-webui-8662`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/8662 |
| issue | #8660 (created 2026-10-31) |
| PR created / merged | 2026-10-31 / 2026-10-31 |
| base | `ffad4f596e12d34cd6e2e7b9e14816665d1992be` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 12 / 2 |
| test files | tests/test_issue8660_agent_update_waits_for_gateway_runs.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
