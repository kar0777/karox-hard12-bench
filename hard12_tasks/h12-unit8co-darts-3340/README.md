# HARD12 task `h12-unit8co-darts-3340`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3340 |
| issue | #3294 (created 2026-10-24) |
| PR created / merged | 2026-11-05 / 2026-11-05 |
| base | `15c087e34d7e34e107c44316782ddec3d1772846` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 1 / 20 |
| test files | darts/tests/models/forecasting/test_4theta.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
