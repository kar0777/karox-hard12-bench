# HARD12 task `h12-mempalace-mempalace-1780`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/1780 |
| issue | #1778 (created 2026-06-11) |
| PR created / merged | 2026-06-11 / 2026-06-14 |
| base | `2ec4baec3f0a8d19143422f26d2e6ee7735543a4` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 34 / 183 |
| test files | tests/test_hallways.py, tests/test_hallways_pagination.py, tests/test_hallways_palace_scoped.py, tests/test_mcp_server.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
