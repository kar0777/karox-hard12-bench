# HARD12 task `h12-zauberzeug-nicegui-6074`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6074 |
| issue | #6072 (created 2026-05-21) |
| PR created / merged | 2026-05-21 / 2026-05-21 |
| base | `cb592ec06f327d4c39b6d3a2aadb82ed74ab2c7b` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 25 / 0 |
| test files | tests/test_storage.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
