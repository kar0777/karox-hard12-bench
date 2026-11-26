# HARD12 task `h12-raullenchai-rapid-mlx-1545`

| item | value |
|---|---|
| source | https://github.com/raullenchai/Rapid-MLX/pull/1545 |
| issue | #1534 (created 2026-08-06) |
| PR created / merged | 2026-08-06 / 2026-08-06 |
| base | `6f4bec53024b2c99e5fdebb7cb23272799308eed` |
| image base | `swerebench/sweb.eval.x86_64.raullenchai_1776_rapid-mlx-341_interface:latest` |
| F2P / P2P | 9 / 8 |
| test files | tests/test_pflash_endpoints_only.py, tests/test_pflash_needle.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
