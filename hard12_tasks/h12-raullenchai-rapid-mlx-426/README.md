# HARD12 task `h12-raullenchai-rapid-mlx-426`

| item | value |
|---|---|
| source | https://github.com/raullenchai/Rapid-MLX/pull/426 |
| issue | #425 (created 2026-05-20) |
| PR created / merged | 2026-05-20 / 2026-05-21 |
| base | `00c046a0a4eca7982f50fe54f4b5dfc1532054cb` |
| image base | `swerebench/sweb.eval.x86_64.raullenchai_1776_rapid-mlx-341_interface:latest` |
| F2P / P2P | 2 / 76 |
| test files | tests/test_postprocessor.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
