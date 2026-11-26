# HARD12 task `h12-mempalace-mempalace-2355`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2355 |
| issue | #2325 (created 2026-08-21) |
| PR created / merged | 2026-08-24 / 2026-08-26 |
| base | `88247acf80121aec0179d1a75606b8252329d3a6` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 3 / 377 |
| test files | tests/test_mcp_server.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
