# HARD12 task `h12-a2aproject-a2a-python-1077`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1077 |
| issue | #1038 (created 2026-05-01) |
| PR created / merged | 2026-05-24 / 2026-05-28 |
| base | `d2f2e18702dd6940ecec020cddd76161174574c1` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 1 / 16 |
| test files | tests/server/tasks/test_task_manager.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
