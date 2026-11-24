# HARD12 task `h12-pasteurlabs-tesseract-core-846`

| item | value |
|---|---|
| source | https://github.com/pasteurlabs/tesseract-core/pull/846 |
| issue | #842 (created 2026-10-14) |
| PR created / merged | 2026-10-14 / 2026-10-20 |
| base | `987034c77f2be5782decbe225ffc81a6cd7b9c42` |
| image base | `swerebench/sweb.eval.x86_64.pasteurlabs_1776_tesseract-core-302:latest` |
| F2P / P2P | 4 / 44 |
| test files | tests/conftest.py, tests/runtime_tests/test_serve.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
