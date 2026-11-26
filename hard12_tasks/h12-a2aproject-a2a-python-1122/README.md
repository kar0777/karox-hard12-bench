# HARD12 task `h12-a2aproject-a2a-python-1122`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1122 |
| issue | #1121 (created 2026-07-03) |
| PR created / merged | 2026-07-04 / 2026-07-20 |
| base | `4e3d7249e2316859fe8e9b85fd688d6d4525d690` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 1 / 25 |
| test files | tests/server/agent_execution/test_active_task.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
