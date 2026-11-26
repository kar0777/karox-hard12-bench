# HARD12 task `h12-pycqa-isort-2576`

| item | value |
|---|---|
| source | https://github.com/PyCQA/isort/pull/2576 |
| issue | #2280 (created 2024-07-18) |
| PR created / merged | 2026-07-06 / 2026-07-12 |
| base | `fd8bd075176d074af69aa6acae7ed89a6a89bb05` |
| image base | `swerebench/sweb.eval.x86_64.pycqa_1776_isort-2491:latest` |
| F2P / P2P | 32 / 313 |
| test files | tests/unit/test_isort.py, tests/unit/test_literal.py, tests/unit/test_regressions.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
