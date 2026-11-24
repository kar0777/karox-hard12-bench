# HARD12 task `h12-python-wheel-build-fromager-1408`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1408 |
| issue | #1401 (created 2026-10-27) |
| PR created / merged | 2026-10-28 / 2026-10-30 |
| base | `2d88bcabea17586a0a82c6a3ef49bdbb86b38876` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 9 / 26 |
| test files | tests/test_find_updates.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
