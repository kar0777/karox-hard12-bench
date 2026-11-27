# HARD12 task `h12-idaholab-montepy-966`

| item | value |
|---|---|
| source | https://github.com/idaholab/MontePy/pull/966 |
| issue | #962 (created 2026-06-05) |
| PR created / merged | 2026-06-10 / 2026-06-16 |
| base | `3adf82ea49a511ac5cbf88595ff507919f82e516` |
| image base | `swerebench/sweb.eval.x86_64.idaholab_1776_montepy-933_interface:latest` |
| F2P / P2P | 3 / 187 |
| test files | tests/test_syntax_parsing.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
