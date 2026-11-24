# HARD12 task `h12-zauberzeug-nicegui-6400`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6400 |
| issue | #6385 (created 2026-10-08) |
| PR created / merged | 2026-10-18 / 2026-10-23 |
| base | `de862b07fa7d65cf56a22e6581e76bef07f4562f` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 4 / 58 |
| test files | tests/test_sub_pages.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
