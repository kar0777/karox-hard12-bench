# HARD12 task `h12-sympy-sympy-30924`

| item | value |
|---|---|
| source | https://github.com/sympy/sympy/pull/30924 |
| issue | #30874 (created 2026-10-29) |
| PR created / merged | 2026-11-02 / 2026-11-05 |
| base | `8e682d837bbc05f630442672de62c8fb455a3821` |
| image base | `swerebench/sweb.eval.x86_64.sympy_1776_sympy-28660:latest` |
| F2P / P2P | 3 / 63 |
| test files | sympy/core/tests/test_evalf.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
