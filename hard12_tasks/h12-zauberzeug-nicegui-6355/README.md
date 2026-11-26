# HARD12 task `h12-zauberzeug-nicegui-6355`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6355 |
| issue | #6341 (created 2026-09-13) |
| PR created / merged | 2026-09-24 / 2026-10-02 |
| base | `255fb9b1812ca50399b4731bf27e086433d78535` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 31 |
| test files | tests/test_storage.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
