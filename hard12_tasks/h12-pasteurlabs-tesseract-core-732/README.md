# HARD12 task `h12-pasteurlabs-tesseract-core-732`

| item | value |
|---|---|
| source | https://github.com/pasteurlabs/tesseract-core/pull/732 |
| issue | #717 (created 2026-09-01) |
| PR created / merged | 2026-09-05 / 2026-09-07 |
| base | `cacde922fa0a119c4d2102c6a1570655bff57f9d` |
| image base | `swerebench/sweb.eval.x86_64.pasteurlabs_1776_tesseract-core-302:latest` |
| F2P / P2P | 1 / 25 |
| test files | tests/runtime_tests/test_serve.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
