# HARD12 task `h12-sympy-sympy-30854`

| item | value |
|---|---|
| source | https://github.com/sympy/sympy/pull/30854 |
| issue | #7769 (created 2014-07-22) |
| PR created / merged | 2026-10-26 / 2026-10-30 |
| base | `bfb177ed523cfac92135da1c52997e1313d04fde` |
| image base | `swerebench/sweb.eval.x86_64.sympy_1776_sympy-28660:latest` |
| F2P / P2P | 2 / 230 |
| test files | sympy/simplify/tests/test_simplify.py, sympy/simplify/tests/test_trigsimp.py, sympy/solvers/tests/test_solvers.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
