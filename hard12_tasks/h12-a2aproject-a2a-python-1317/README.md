# HARD12 task `h12-a2aproject-a2a-python-1317`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1317 |
| issue | #1316 (created 2026-10-05) |
| PR created / merged | 2026-10-05 / 2026-10-06 |
| base | `59dcbfb16f73c7c596e6d60cb700ed71193c5cce` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 2 / 81 |
| test files | tests/server/request_handlers/test_default_request_handler_v2.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
