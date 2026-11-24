# HARD12 task `h12-sympy-sympy-30841`

| item | value |
|---|---|
| source | https://github.com/sympy/sympy/pull/30841 |
| issue | #30756 (created 2026-10-16) |
| PR created / merged | 2026-10-25 / 2026-10-27 |
| base | `9a1e9e24af36d4c190ce7981727340de7110a663` |
| image base | `swerebench/sweb.eval.x86_64.sympy_1776_sympy-28660:latest` |
| F2P / P2P | 2 / 22 |
| test files | sympy/calculus/tests/test_singularities.py, sympy/calculus/tests/test_util.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
