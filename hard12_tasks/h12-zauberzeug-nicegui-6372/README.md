# HARD12 task `h12-zauberzeug-nicegui-6372`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6372 |
| issue | #6331 (created 2026-09-10) |
| PR created / merged | 2026-10-05 / 2026-10-20 |
| base | `19cc869c5ea4ac55fdde55ab023ba4fbf1ead19f` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 24 |
| test files | tests/test_background_tasks.py, tests/test_timer.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
