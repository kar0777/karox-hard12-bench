# HARD12 task `h12-pasteurlabs-tesseract-core-730`

| item | value |
|---|---|
| source | https://github.com/pasteurlabs/tesseract-core/pull/730 |
| issue | #729 (created 2026-09-05) |
| PR created / merged | 2026-09-05 / 2026-09-14 |
| base | `e6f54b7557767de1c843b9403385450cc50242eb` |
| image base | `swerebench/sweb.eval.x86_64.pasteurlabs_1776_tesseract-core-302:latest` |
| F2P / P2P | 2 / 19 |
| test files | tests/runtime_tests/test_schema_types.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
