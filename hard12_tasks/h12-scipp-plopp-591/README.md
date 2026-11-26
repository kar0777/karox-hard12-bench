# HARD12 task `h12-scipp-plopp-591`

| item | value |
|---|---|
| source | https://github.com/scipp/plopp/pull/591 |
| issue | #590 (created 2026-07-28) |
| PR created / merged | 2026-07-28 / 2026-07-31 |
| base | `1c52f1e386ce53812e8ad4c103c5eae9678ed248` |
| image base | `swerebench/sweb.eval.x86_64.scipp_1776_plopp-513:latest` |
| F2P / P2P | 4 / 104 |
| test files | tests/backends/matplotlib/mpl_line_test.py, tests/backends/matplotlib/mpl_plot_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
