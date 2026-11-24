# HARD12 task `h12-a2aproject-a2a-python-1424`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1424 |
| issue | #1423 (created 2026-11-04) |
| PR created / merged | 2026-11-04 / 2026-11-05 |
| base | `5e0d415761d3f596f0a4354e3a265c1343b0e887` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 1 / 31 |
| test files | tests/compat/v0_3/test_rest_transport.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
