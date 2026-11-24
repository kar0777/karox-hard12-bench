# HARD12 task `h12-a2aproject-a2a-python-1458`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1458 |
| issue | #1457 (created 2026-11-12) |
| PR created / merged | 2026-11-12 / 2026-11-13 |
| base | `239999307b365ff99db98495fc78683868976c1e` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 2 / 38 |
| test files | tests/compat/v0_3/test_rest_transport.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
