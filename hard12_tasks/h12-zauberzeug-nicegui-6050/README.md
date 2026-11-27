# HARD12 task `h12-zauberzeug-nicegui-6050`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6050 |
| issue | #6044 (created 2026-05-08) |
| PR created / merged | 2026-05-13 / 2026-06-09 |
| base | `e53fb933f13cc473224f79f9b7466d4e825573c3` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 25 |
| test files | tests/test_storage.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
