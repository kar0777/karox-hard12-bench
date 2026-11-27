# HARD12 task `h12-zauberzeug-nicegui-6146`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6146 |
| issue | #6145 (created 2026-07-07) |
| PR created / merged | 2026-07-07 / 2026-07-08 |
| base | `4c5375de1d83ba274e5d769ce7caf57293767fcd` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 26 |
| test files | tests/test_storage.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
