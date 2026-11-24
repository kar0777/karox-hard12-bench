# HARD12 task `h12-python-wheel-build-fromager-1377`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1377 |
| issue | #1376 (created 2026-10-16) |
| PR created / merged | 2026-10-16 / 2026-10-20 |
| base | `45241aadd284fd9514fc5c250e9ec0ceccfd91a6` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 1 / 15 |
| test files | tests/test_sbom.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
