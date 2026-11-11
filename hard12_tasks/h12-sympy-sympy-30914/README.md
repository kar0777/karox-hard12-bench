# HARD12 task `h12-sympy-sympy-30914`

| item | value |
|---|---|
| source | https://github.com/sympy/sympy/pull/30914 |
| issue | #30913 (created 2026-11-01) |
| PR created / merged | 2026-11-01 / 2026-11-03 |
| base | `eb51b9b1eb2d98b7bdedc440bb4944b95f96d1de` |
| image base | `swerebench/sweb.eval.x86_64.sympy_1776_sympy-28660:latest` |
| F2P / P2P | 1 / 175 |
| test files | sympy/series/tests/test_limits.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
