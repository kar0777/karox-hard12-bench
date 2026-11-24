# HARD12 task `h12-zauberzeug-nicegui-6500`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6500 |
| issue | #6499 (created 2026-11-11) |
| PR created / merged | 2026-11-12 / 2026-11-23 |
| base | `589f2d570df0616f33b7fba42e15139afd799179` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 2 / 38 |
| test files | tests/test_binding.py, tests/test_events.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
