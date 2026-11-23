# HARD12 task `h12-nesquena-hermes-webui-9002`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/9002 |
| issue | #9000 (created 2026-11-11) |
| PR created / merged | 2026-11-11 / 2026-11-11 |
| base | `66854e84b25e52ba791a8df978332d7d146ba3d2` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 2 / 2 |
| test files | tests/test_issue9000_resolver_output_guard.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
