# HARD12 task `h12-sympy-sympy-30165`

| item | value |
|---|---|
| source | https://github.com/sympy/sympy/pull/30165 |
| issue | #29986 (created 2026-06-30) |
| PR created / merged | 2026-07-29 / 2026-08-20 |
| base | `81b519fabdbbc8e82db154dd271100ec7fb7ef32` |
| image base | `swerebench/sweb.eval.x86_64.sympy_1776_sympy-28660:latest` |
| F2P / P2P | 6 / 230 |
| test files | sympy/integrals/tests/test_integrals.py, sympy/integrals/tests/test_manual.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
