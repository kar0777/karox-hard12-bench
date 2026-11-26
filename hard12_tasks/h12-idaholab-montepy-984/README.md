# HARD12 task `h12-idaholab-montepy-984`

| item | value |
|---|---|
| source | https://github.com/idaholab/MontePy/pull/984 |
| issue | #964 (created 2026-06-07) |
| PR created / merged | 2026-07-13 / 2026-07-16 |
| base | `92028db8fe715ceb17c8ed1dafe3cc9bf2118931` |
| image base | `swerebench/sweb.eval.x86_64.idaholab_1776_montepy-933_interface:latest` |
| F2P / P2P | 1 / 23 |
| test files | tests/test_cell_problem.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
