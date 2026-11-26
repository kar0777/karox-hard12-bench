# HARD12 task `h12-zauberzeug-nicegui-6337`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6337 |
| issue | #6301 (created 2026-08-21) |
| PR created / merged | 2026-09-11 / 2026-09-15 |
| base | `3f5af28fdb8edb9d91a3ac9a92d17cc233725ccc` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 3 / 7 |
| test files | tests/test_lifecycle.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
