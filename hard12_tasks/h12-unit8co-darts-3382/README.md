# HARD12 task `h12-unit8co-darts-3382`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3382 |
| issue | #3379 (created 2026-11-16) |
| PR created / merged | 2026-11-16 / 2026-11-16 |
| base | `21934d8f3260683be7b5cf4d1166270c615eaacd` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 1 / 334 |
| test files | darts/tests/test_timeseries.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
