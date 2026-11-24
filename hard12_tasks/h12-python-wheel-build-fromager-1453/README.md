# HARD12 task `h12-python-wheel-build-fromager-1453`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1453 |
| issue | #1375 (created 2026-10-16) |
| PR created / merged | 2026-11-04 / 2026-11-05 |
| base | `70aa4594b9e3c5198e56d1e520698f19881bc87d` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 3 / 40 |
| test files | tests/test_sbom.py, tests/test_wheels.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
