# HARD12 task `h12-pycqa-isort-2794`

| item | value |
|---|---|
| source | https://github.com/PyCQA/isort/pull/2794 |
| issue | #2793 (created 2026-11-15) |
| PR created / merged | 2026-11-15 / 2026-11-16 |
| base | `eb62da318ea543b82340f3d0a52bc0509c7e626e` |
| image base | `swerebench/sweb.eval.x86_64.pycqa_1776_isort-2491:latest` |
| F2P / P2P | 1 / 138 |
| test files | tests/unit/test_regressions.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
