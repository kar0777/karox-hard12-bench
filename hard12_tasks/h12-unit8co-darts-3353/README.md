# HARD12 task `h12-unit8co-darts-3353`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3353 |
| issue | #3336 (created 2026-11-04) |
| PR created / merged | 2026-11-11 / 2026-11-13 |
| base | `bbe59223ca9f79d8c3f06a686d3f0f007b348f31` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 11 / 87 |
| test files | darts/tests/models/forecasting/test_ensemble_models.py, darts/tests/models/forecasting/test_probabilistic_models.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
