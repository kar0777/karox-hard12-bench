# HARD12 task `h12-unit8co-darts-3358`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3358 |
| issue | #3344 (created 2026-11-07) |
| PR created / merged | 2026-11-11 / 2026-11-12 |
| base | `0fc705f1e0e286c1856983211b5fd0a6867c995a` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 21 / 1478 |
| test files | darts/tests/models/forecasting/test_sklearn_models.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
