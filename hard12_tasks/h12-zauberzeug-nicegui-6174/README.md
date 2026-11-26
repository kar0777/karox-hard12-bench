# HARD12 task `h12-zauberzeug-nicegui-6174`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6174 |
| issue | #6173 (created 2026-07-23) |
| PR created / merged | 2026-07-23 / 2026-07-23 |
| base | `9a088b2ec23dc4896741b1908d878727aff13f7c` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 3 / 26 |
| test files | tests/test_storage.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
