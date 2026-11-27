# HARD12 task `h12-pasteurlabs-tesseract-core-600`

| item | value |
|---|---|
| source | https://github.com/pasteurlabs/tesseract-core/pull/600 |
| issue | #175 (created 2025-05-26) |
| PR created / merged | 2026-05-19 / 2026-06-17 |
| base | `0a925a7313068e2321129e83fe5eea05ff5ce4b0` |
| image base | `swerebench/sweb.eval.x86_64.pasteurlabs_1776_tesseract-core-302:latest` |
| F2P / P2P | 1 / 13 |
| test files | tests/endtoend_tests/test_examples.py, tests/sdk_tests/test_api_parse.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
