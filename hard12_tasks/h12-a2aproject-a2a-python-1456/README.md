# HARD12 task `h12-a2aproject-a2a-python-1456`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1456 |
| issue | #1432 (created 2026-11-07) |
| PR created / merged | 2026-11-12 / 2026-11-13 |
| base | `1ff86d597caddd90cb22a1a7264097f64b287905` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 12 / 99 |
| test files | tests/client/transports/test_http_helpers.py, tests/client/transports/test_jsonrpc_client.py, tests/client/transports/test_rest_client.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
