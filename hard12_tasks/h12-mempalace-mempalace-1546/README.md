# HARD12 task `h12-mempalace-mempalace-1546`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/1546 |
| issue | #1473 (created 2026-05-12) |
| PR created / merged | 2026-05-18 / 2026-05-18 |
| base | `34d8dde969d9c719f1d5c5ae65015dfe415b5d4c` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 1 / 154 |
| test files | tests/test_mcp_server.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
