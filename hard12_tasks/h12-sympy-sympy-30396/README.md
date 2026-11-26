# HARD12 task `h12-sympy-sympy-30396`

| item | value |
|---|---|
| source | https://github.com/sympy/sympy/pull/30396 |
| issue | #30395 (created 2026-09-02) |
| PR created / merged | 2026-09-03 / 2026-09-27 |
| base | `e0e25c8eaab46155ee7c35c783e3f6f41e147b9b` |
| image base | `swerebench/sweb.eval.x86_64.sympy_1776_sympy-28660:latest` |
| F2P / P2P | 4 / 46 |
| test files | sympy/printing/tests/test_numpy.py, sympy/printing/tests/test_pycode.py, sympy/printing/tests/test_tensorflow.py, sympy/tensor/array/expressions/tests/test_convert_indexed_to_array.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
