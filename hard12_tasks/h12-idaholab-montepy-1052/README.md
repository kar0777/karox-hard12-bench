# HARD12 task `h12-idaholab-montepy-1052`

| item | value |
|---|---|
| source | https://github.com/idaholab/MontePy/pull/1052 |
| issue | #1051 (created 2026-11-05) |
| PR created / merged | 2026-11-05 / 2026-11-10 |
| base | `cb5841ae1bdee06cbb4b085305530a551fe9c2d7` |
| image base | `swerebench/sweb.eval.x86_64.idaholab_1776_montepy-933_interface:latest` |
| F2P / P2P | 4 / 110 |
| test files | tests/test_integration.py, tests/test_universe_integration.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
