# HARD12 task `h12-unit8co-darts-3225`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3225 |
| issue | #3224 (created 2026-09-29) |
| PR created / merged | 2026-09-29 / 2026-10-08 |
| base | `cf9ad53215eaa36f624c389c9170f6b01fd3f970` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 1 / 400 |
| test files | darts/tests/metrics/test_metrics.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
