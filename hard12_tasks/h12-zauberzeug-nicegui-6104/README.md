# HARD12 task `h12-zauberzeug-nicegui-6104`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6104 |
| issue | #5185 (created 2025-09-29) |
| PR created / merged | 2026-06-11 / 2026-06-12 |
| base | `fbc240722032560d21c92128372e65298b29abe7` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 15 |
| test files | tests/test_input.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
