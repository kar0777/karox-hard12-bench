# HARD12 task `h12-a2aproject-a2a-python-1106`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1106 |
| issue | #1067 (created 2026-05-16) |
| PR created / merged | 2026-06-16 / 2026-07-20 |
| base | `86c6b0d7dd3ea83efb808de348a0021677b2f0b2` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 3 / 54 |
| test files | tests/server/request_handlers/test_default_request_handler_v2.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
