# HARD12 task `h12-unit8co-darts-3217`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3217 |
| issue | #2225 (created 2024-02-12) |
| PR created / merged | 2026-09-27 / 2026-09-28 |
| base | `3ecc58e962f0e6b6df22a96881d7334cb4e4cca2` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 1 / 80 |
| test files | darts/tests/models/forecasting/test_local_forecasting_models.py, darts/tests/optional_deps/test_optuna.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
