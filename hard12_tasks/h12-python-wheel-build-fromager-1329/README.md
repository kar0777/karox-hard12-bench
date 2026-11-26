# HARD12 task `h12-python-wheel-build-fromager-1329`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1329 |
| issue | #1315 (created 2026-09-03) |
| PR created / merged | 2026-09-15 / 2026-10-06 |
| base | `82e125032e04e5fa724ed13ebbb2e8660f2cdbdd` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 2 / 57 |
| test files | tests/test_sources.py, tests/test_tarballs.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
