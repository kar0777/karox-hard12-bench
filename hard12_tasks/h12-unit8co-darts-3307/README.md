# HARD12 task `h12-unit8co-darts-3307`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3307 |
| issue | #3296 (created 2026-10-24) |
| PR created / merged | 2026-10-26 / 2026-10-27 |
| base | `1453ffb8eb48aadeffb91d41ae3538dde4793196` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 1 / 326 |
| test files | darts/tests/test_timeseries.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
