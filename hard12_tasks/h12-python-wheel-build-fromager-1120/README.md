# HARD12 task `h12-python-wheel-build-fromager-1120`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1120 |
| issue | #1118 (created 2026-05-06) |
| PR created / merged | 2026-05-06 / 2026-05-12 |
| base | `abfdf973d5f48b82cf412c686a024629de3f5e90` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 8 / 33 |
| test files | tests/test_http_retry.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
