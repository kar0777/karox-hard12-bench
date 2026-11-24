# HARD12 task `h12-a2aproject-a2a-python-1476`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1476 |
| issue | #1475 (created 2026-11-15) |
| PR created / merged | 2026-11-15 / 2026-11-22 |
| base | `06cd52892e456ce7e9f81f400f816a729a60dece` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 3 / 63 |
| test files | tests/client/transports/test_jsonrpc_client.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
