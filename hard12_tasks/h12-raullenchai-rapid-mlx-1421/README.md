# HARD12 task `h12-raullenchai-rapid-mlx-1421`

| item | value |
|---|---|
| source | https://github.com/raullenchai/Rapid-MLX/pull/1421 |
| issue | #1255 (created 2026-07-27) |
| PR created / merged | 2026-08-03 / 2026-08-03 |
| base | `7b337e9d73a471fd2f40a2bf1e9bf4b05965b921` |
| image base | `swerebench/sweb.eval.x86_64.raullenchai_1776_rapid-mlx-341_interface:latest` |
| F2P / P2P | 5 / 52 |
| test files | tests/test_doctor_env_health.py, tests/test_vision_extra_install.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
