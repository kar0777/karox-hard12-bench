# HARD12 task `h12-unit8co-darts-3327`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3327 |
| issue | #2494 (created 2024-08-09) |
| PR created / merged | 2026-10-31 / 2026-11-04 |
| base | `20af2c8db7b53c18416dcf9d611ca9ff0a561289` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 1 / 1496 |
| test files | darts/tests/models/forecasting/test_sklearn_models.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
