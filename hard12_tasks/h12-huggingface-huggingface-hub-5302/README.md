# HARD12 task `h12-huggingface-huggingface-hub-5302`

| item | value |
|---|---|
| source | https://github.com/huggingface/huggingface_hub/pull/5302 |
| issue | #5293 (created 2026-11-01) |
| PR created / merged | 2026-11-04 / 2026-11-04 |
| base | `bd7e65e442c5baeecaa0c946b9a9eb9f31d93fae` |
| image base | `swerebench/sweb.eval.x86_64.huggingface_1776_huggingface_hub-4056:latest` |
| F2P / P2P | 3 / 401 |
| test files | tests/test_cli.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
