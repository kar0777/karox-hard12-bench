# HARD12 task `h12-a2aproject-a2a-python-1366`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1366 |
| issue | #1351 (created 2026-10-18) |
| PR created / merged | 2026-10-22 / 2026-10-23 |
| base | `30b6d5067a9256447e3d5324163b091fc4bbad74` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 2 / 124 |
| test files | tests/server/agent_execution/test_active_task.py, tests/server/request_handlers/test_default_request_handler_v2.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
