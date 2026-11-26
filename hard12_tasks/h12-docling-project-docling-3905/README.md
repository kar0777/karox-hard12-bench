# HARD12 task `h12-docling-project-docling-3905`

| item | value |
|---|---|
| source | https://github.com/docling-project/docling/pull/3905 |
| issue | #3733 (created 2026-07-02) |
| PR created / merged | 2026-07-28 / 2026-07-29 |
| base | `873f990203ac3195b0142f5564eea13e59c1a312` |
| image base | `swerebench/sweb.eval.x86_64.docling-project_1776_docling-2998:latest` |
| F2P / P2P | 3 / 0 |
| test files | tests/test_version.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
