# HARD12 task `h12-a2aproject-a2a-python-1466`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1466 |
| issue | #1465 (created 2026-11-13) |
| PR created / merged | 2026-11-13 / 2026-11-14 |
| base | `39329820e31fe4977e63cf07ce4b2c2b73066a9e` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 1 / 5 |
| test files | tests/compat/v0_3/test_grpc_transport.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
