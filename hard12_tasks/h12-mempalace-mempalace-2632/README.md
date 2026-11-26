# HARD12 task `h12-mempalace-mempalace-2632`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2632 |
| issue | #2618 (created 2026-09-29) |
| PR created / merged | 2026-10-02 / 2026-10-10 |
| base | `5ea40d30caf0ed2ff6e49623e386a0863b28edaa` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 1 / 40 |
| test files | tests/mcp/test_guards.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
