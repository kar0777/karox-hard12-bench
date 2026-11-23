# HARD12 task `h12-zauberzeug-nicegui-6509`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6509 |
| issue | #6508 (created 2026-11-15) |
| PR created / merged | 2026-11-15 / 2026-11-19 |
| base | `884eb1c38e58f976bce451d4e19cf898b78dfefa` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 6 / 8 |
| test files | tests/test_awaitable_response.py, tests/test_background_tasks.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
