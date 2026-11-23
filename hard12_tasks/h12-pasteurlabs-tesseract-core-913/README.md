# HARD12 task `h12-pasteurlabs-tesseract-core-913`

| item | value |
|---|---|
| source | https://github.com/pasteurlabs/tesseract-core/pull/913 |
| issue | #911 (created 2026-11-06) |
| PR created / merged | 2026-11-06 / 2026-11-12 |
| base | `00434348b328b277691f8632090071080d864ec4` |
| image base | `swerebench/sweb.eval.x86_64.pasteurlabs_1776_tesseract-core-302:latest` |
| F2P / P2P | 5 / 52 |
| test files | tests/runtime_tests/test_schema_generation.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
