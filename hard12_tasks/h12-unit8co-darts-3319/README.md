# HARD12 task `h12-unit8co-darts-3319`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3319 |
| issue | #3310 (created 2026-10-27) |
| PR created / merged | 2026-10-28 / 2026-10-29 |
| base | `580358e6e4f88f505116d2fda7d6dff4c0e33c78` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 2 / 485 |
| test files | darts/tests/metrics/test_metrics.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
