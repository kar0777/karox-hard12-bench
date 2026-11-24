# HARD12 task `h12-zauberzeug-nicegui-6473`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6473 |
| issue | #6472 (created 2026-11-04) |
| PR created / merged | 2026-11-05 / 2026-11-06 |
| base | `69edb3faa8e792548e5163373d34f82a00800d26` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 9 |
| test files | tests/test_awaitable_response.py, tests/test_javascript.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
