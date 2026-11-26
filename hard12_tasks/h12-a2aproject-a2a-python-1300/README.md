# HARD12 task `h12-a2aproject-a2a-python-1300`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1300 |
| issue | #1299 (created 2026-10-02) |
| PR created / merged | 2026-10-02 / 2026-10-02 |
| base | `5a1a004ecd9e3051223923f7e2db8c15401a20f7` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 8 / 63 |
| test files | tests/client/transports/test_rest_client.py, tests/compat/v0_3/test_rest_transport.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
