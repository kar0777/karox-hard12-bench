# HARD12 task `h12-getmoto-moto-10070`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10070 |
| issue | #8722 (created 2025-03-27) |
| PR created / merged | 2026-06-18 / 2026-06-26 |
| base | `70ddf33599619e4a48e61881e6d886287cdf7226` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 4 / 104 |
| test files | tests/test_ecs/test_ecs.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
