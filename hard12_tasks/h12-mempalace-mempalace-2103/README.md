# HARD12 task `h12-mempalace-mempalace-2103`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2103 |
| issue | #2101 (created 2026-07-29) |
| PR created / merged | 2026-07-29 / 2026-08-02 |
| base | `aa89bd82272f55381206c83b6f306e79351824eb` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 5 / 300 |
| test files | tests/test_mcp_http_transport.py, tests/test_mcp_server.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
