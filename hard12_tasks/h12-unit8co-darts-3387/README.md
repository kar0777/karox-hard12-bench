# HARD12 task `h12-unit8co-darts-3387`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3387 |
| issue | #1462 (created 2023-01-03) |
| PR created / merged | 2026-11-16 / 2026-11-17 |
| base | `d326ea440f168b62d895094d0967d1646ba4b108` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 7 / 151 |
| test files | darts/tests/models/forecasting/test_backtesting.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
