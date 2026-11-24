# HARD12 task `h12-mempalace-mempalace-2882`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2882 |
| issue | #2620 (created 2026-09-29) |
| PR created / merged | 2026-10-23 / 2026-10-31 |
| base | `f41e8e75ddaadf5588d5127715fa531d79eadb45` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 17 / 109 |
| test files | tests/mcp/test_protocol.py, tests/test_mcp_http_call_timing.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
