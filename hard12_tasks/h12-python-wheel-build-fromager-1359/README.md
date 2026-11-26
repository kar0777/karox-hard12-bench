# HARD12 task `h12-python-wheel-build-fromager-1359`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1359 |
| issue | #1358 (created 2026-10-05) |
| PR created / merged | 2026-10-05 / 2026-10-05 |
| base | `1e3c39d71ffd0bc1832952cf77af06e4cc4be92b` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 2 / 51 |
| test files | tests/test_cooldown.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
