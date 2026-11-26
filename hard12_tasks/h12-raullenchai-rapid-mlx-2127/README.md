# HARD12 task `h12-raullenchai-rapid-mlx-2127`

| item | value |
|---|---|
| source | https://github.com/raullenchai/Rapid-MLX/pull/2127 |
| issue | #2125 (created 2026-08-19) |
| PR created / merged | 2026-08-19 / 2026-08-19 |
| base | `123e5d6f7304f83c3536e56fab1889fc7c1c571d` |
| image base | `swerebench/sweb.eval.x86_64.raullenchai_1776_rapid-mlx-341_interface:latest` |
| F2P / P2P | 5 / 14 |
| test files | tests/test_serve_host_loopback_default.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
