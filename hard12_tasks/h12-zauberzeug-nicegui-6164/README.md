# HARD12 task `h12-zauberzeug-nicegui-6164`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6164 |
| issue | #6163 (created 2026-07-21) |
| PR created / merged | 2026-07-22 / 2026-07-22 |
| base | `5e936383cd1cd31bda1c59e04e3144a1e233e1cc` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 17 |
| test files | tests/test_observables.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
