# HARD12 task `h12-zauberzeug-nicegui-6271`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6271 |
| issue | #6232 (created 2026-08-03) |
| PR created / merged | 2026-08-07 / 2026-08-27 |
| base | `77391cfebe1b7d2a862453459184c2c6e9d30cde` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 5 / 38 |
| test files | tests/test_button.py, tests/test_page.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
