# HARD12 task `h12-docling-project-docling-5087`

| item | value |
|---|---|
| source | https://github.com/docling-project/docling/pull/5087 |
| issue | #5086 (created 2026-10-29) |
| PR created / merged | 2026-10-29 / 2026-10-30 |
| base | `8f7ae54409583908f06a2172d260e71b964cc4dd` |
| image base | `swerebench/sweb.eval.x86_64.docling-project_1776_docling-2998:latest` |
| F2P / P2P | 2 / 55 |
| test files | tests/test_backend_iwork_numbers.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
