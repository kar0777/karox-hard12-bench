# HARD12 task `h12-a2aproject-a2a-python-1172`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1172 |
| issue | #1159 (created 2026-08-03) |
| PR created / merged | 2026-08-09 / 2026-08-21 |
| base | `0c2126fbf1e2b418872181ce2ae200f972b4c202` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 7 / 205 |
| test files | tests/integration/test_scenarios.py, tests/server/agent_execution/test_active_task.py, tests/server/agent_execution/test_active_task_registry.py, tests/server/request_handlers/test_default_request_handler_v2.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
