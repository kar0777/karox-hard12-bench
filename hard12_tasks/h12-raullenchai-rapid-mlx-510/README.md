# HARD12 task `h12-raullenchai-rapid-mlx-510`

| item | value |
|---|---|
| source | https://github.com/raullenchai/Rapid-MLX/pull/510 |
| issue | #470 (created 2026-05-23) |
| PR created / merged | 2026-06-04 / 2026-06-04 |
| base | `74c1316aaae860e5047cae5374828e306308907b` |
| image base | `swerebench/sweb.eval.x86_64.raullenchai_1776_rapid-mlx-341_interface:latest` |
| F2P / P2P | 1 / 7 |
| test files | tests/test_sampling_params_passthrough.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
