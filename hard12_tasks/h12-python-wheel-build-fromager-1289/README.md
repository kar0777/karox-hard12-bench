# HARD12 task `h12-python-wheel-build-fromager-1289`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1289 |
| issue | #1288 (created 2026-08-05) |
| PR created / merged | 2026-08-05 / 2026-08-07 |
| base | `925a19e084ae4392202d25fd9d5966f993e15a5d` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 8 / 55 |
| test files | tests/test_bootstrap_requirement_resolver.py, tests/test_cooldown.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
