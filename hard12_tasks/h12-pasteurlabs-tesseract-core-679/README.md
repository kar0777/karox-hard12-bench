# HARD12 task `h12-pasteurlabs-tesseract-core-679`

| item | value |
|---|---|
| source | https://github.com/pasteurlabs/tesseract-core/pull/679 |
| issue | #678 (created 2026-08-20) |
| PR created / merged | 2026-08-20 / 2026-08-25 |
| base | `c379c12974cc5bf86ca126d8f46848828b70d5a9` |
| image base | `swerebench/sweb.eval.x86_64.pasteurlabs_1776_tesseract-core-302:latest` |
| F2P / P2P | 16 / 99 |
| test files | tests/sdk_tests/test_cli.py, tests/sdk_tests/test_engine.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
