# HARD12 task `h12-sympy-sympy-30684`

| item | value |
|---|---|
| source | https://github.com/sympy/sympy/pull/30684 |
| issue | #23183 (created 2022-03-01) |
| PR created / merged | 2026-10-06 / 2026-10-07 |
| base | `319ea7a6186edf88bc23d502917242b10314ae51` |
| image base | `swerebench/sweb.eval.x86_64.sympy_1776_sympy-28660:latest` |
| F2P / P2P | 1 / 0 |
| test files | sympy/interactive/tests/test_interactive.py, sympy/interactive/tests/test_ipython.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
