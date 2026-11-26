# HARD12 task `h12-mempalace-mempalace-2211`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2211 |
| issue | #2210 (created 2026-08-10) |
| PR created / merged | 2026-08-10 / 2026-08-11 |
| base | `8516db7fbc7f0840bf67132c5bf95c6e446d6acc` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 4 / 13 |
| test files | tests/test_mcp_mine.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
