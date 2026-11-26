# HARD12 task `h12-zauberzeug-nicegui-6326`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6326 |
| issue | #6318 (created 2026-09-01) |
| PR created / merged | 2026-09-08 / 2026-09-10 |
| base | `0dae9865ab6e5831c4ea3317e7ea3ae4f7b874b9` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 1 / 5 |
| test files | tests/test_lazy_imports.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
