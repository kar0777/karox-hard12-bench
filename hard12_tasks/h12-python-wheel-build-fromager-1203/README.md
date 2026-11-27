# HARD12 task `h12-python-wheel-build-fromager-1203`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1203 |
| issue | #1198 (created 2026-06-17) |
| PR created / merged | 2026-06-22 / 2026-06-22 |
| base | `24af91e60850939a4d0520acd39b33c60ffc9ab3` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 8 / 98 |
| test files | tests/test_bootstrapper.py, tests/test_bootstrapper_iterative.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
