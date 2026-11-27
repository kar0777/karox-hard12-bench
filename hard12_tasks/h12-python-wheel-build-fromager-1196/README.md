# HARD12 task `h12-python-wheel-build-fromager-1196`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1196 |
| issue | #1195 (created 2026-06-11) |
| PR created / merged | 2026-06-11 / 2026-06-15 |
| base | `64399e0ab3e86b0eb609442dbf07955db9828397` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 2 / 72 |
| test files | tests/test_bootstrapper_iterative.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
