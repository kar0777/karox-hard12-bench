# HARD12 task `h12-python-wheel-build-fromager-1386`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1386 |
| issue | #1383 (created 2026-10-19) |
| PR created / merged | 2026-10-21 / 2026-11-09 |
| base | `e9b86d8a1970945918d0ba8f7bd388c61b327e29` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 5 / 17 |
| test files | tests/test_sbom.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
