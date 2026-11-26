# HARD12 task `h12-a2aproject-a2a-python-1212`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1212 |
| issue | #1211 (created 2026-08-27) |
| PR created / merged | 2026-08-27 / 2026-08-31 |
| base | `3eb88e223e62ec510128a8fb51e3ccfe7aa6d596` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 2 / 38 |
| test files | tests/server/routes/test_jsonrpc_dispatcher.py, tests/server/routes/test_rest_dispatcher.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
