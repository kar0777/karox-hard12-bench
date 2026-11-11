# HARD12 task `h12-zauberzeug-nicegui-6485`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6485 |
| issue | #6469 (created 2026-11-04) |
| PR created / merged | 2026-11-06 / 2026-11-06 |
| base | `09c449977f94d4fc03bbb77756e5dd8121b6db2b` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 9 |
| test files | tests/test_user_simulation_context.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
