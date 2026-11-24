# HARD12 task `h12-zauberzeug-nicegui-6478`

| item | value |
|---|---|
| source | https://github.com/zauberzeug/nicegui/pull/6478 |
| issue | #6466 (created 2026-11-03) |
| PR created / merged | 2026-11-05 / 2026-11-06 |
| base | `824bb9a77b7b6162a5b32661bfcd1faf4f95b806` |
| image base | `swerebench/sweb.eval.x86_64.zauberzeug_1776_nicegui-5914:latest` |
| F2P / P2P | 2 / 66 |
| test files | tests/test_root_page.py, tests/test_sub_pages.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
