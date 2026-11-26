# HARD12 task `h12-idaholab-montepy-975`

| item | value |
|---|---|
| source | https://github.com/idaholab/MontePy/pull/975 |
| issue | #500 (created 2024-08-22) |
| PR created / merged | 2026-06-27 / 2026-07-22 |
| base | `257a8282f2a82559136479f1c1dade93f0b2f921` |
| image base | `swerebench/sweb.eval.x86_64.idaholab_1776_montepy-933_interface:latest` |
| F2P / P2P | 3 / 231 |
| test files | tests/test_syntax_parsing.py, tests/test_universe.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
