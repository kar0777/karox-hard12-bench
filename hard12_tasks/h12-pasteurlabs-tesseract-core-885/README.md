# HARD12 task `h12-pasteurlabs-tesseract-core-885`

| item | value |
|---|---|
| source | https://github.com/pasteurlabs/tesseract-core/pull/885 |
| issue | #883 (created 2026-10-29) |
| PR created / merged | 2026-10-31 / 2026-11-01 |
| base | `f97585b45cd721769e047a77392afe2509fbc827` |
| image base | `swerebench/sweb.eval.x86_64.pasteurlabs_1776_tesseract-core-302:latest` |
| F2P / P2P | 4 / 101 |
| test files | tests/runtime_tests/test_core.py, tests/runtime_tests/test_runtime_cli.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
