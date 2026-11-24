# HARD12 task `h12-a2aproject-a2a-python-1354`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1354 |
| issue | #1341 (created 2026-10-15) |
| PR created / merged | 2026-10-19 / 2026-10-21 |
| base | `cdb479957e81600f68f946f8ff0122667673cb35` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 7 / 98 |
| test files | tests/client/transports/test_jsonrpc_client.py, tests/client/transports/test_rest_client.py, tests/utils/test_proto_utils.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
