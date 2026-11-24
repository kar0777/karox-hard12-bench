# HARD12 task `h12-docling-project-docling-4949`

| item | value |
|---|---|
| source | https://github.com/docling-project/docling/pull/4949 |
| issue | #4948 (created 2026-10-21) |
| PR created / merged | 2026-10-21 / 2026-10-26 |
| base | `29caea8381e885872905dc9438f10014368a2a25` |
| image base | `swerebench/sweb.eval.x86_64.docling-project_1776_docling-2998:latest` |
| F2P / P2P | 11 / 30 |
| test files | tests/test_backend_text_encoding.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
