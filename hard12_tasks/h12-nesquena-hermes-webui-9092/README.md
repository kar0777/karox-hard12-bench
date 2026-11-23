# HARD12 task `h12-nesquena-hermes-webui-9092`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/9092 |
| issue | #8965 (created 2026-11-09) |
| PR created / merged | 2026-11-15 / 2026-11-15 |
| base | `5cdb96c6b3f54eafabda6106b3aa8bb85dca32bd` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 5 / 23 |
| test files | tests/test_goal_command_js_behaviour.py, tests/test_goal_command_webui.py, tests/test_goal_gate_refusal_copy.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
