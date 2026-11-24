# HARD12 task `h12-docling-project-docling-5144`

| item | value |
|---|---|
| source | https://github.com/docling-project/docling/pull/5144 |
| issue | #5142 (created 2026-11-02) |
| PR created / merged | 2026-11-02 / 2026-11-03 |
| base | `07154cdc82500058ad9377bac92beed3de820458` |
| image base | `swerebench/sweb.eval.x86_64.docling-project_1776_docling-2998:latest` |
| F2P / P2P | 6 / 69 |
| test files | tests/test_backend_asciidoc.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
