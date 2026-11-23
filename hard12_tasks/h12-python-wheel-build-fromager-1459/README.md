# HARD12 task `h12-python-wheel-build-fromager-1459`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1459 |
| issue | #1421 (created 2026-10-30) |
| PR created / merged | 2026-11-07 / 2026-11-12 |
| base | `d86e4968dbf2c59a3d97d26eb369c8f2a9f512c2` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 1 / 10 |
| test files | tests/test_list_overrides.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
