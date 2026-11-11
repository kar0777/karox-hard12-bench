# HARD12 task `h12-mempalace-mempalace-2898`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2898 |
| issue | #2884 (created 2026-10-24) |
| PR created / merged | 2026-10-25 / 2026-10-31 |
| base | `da6e21fbbebff250193812a5786180bb65cfa459` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 1 / 174 |
| test files | tests/test_hooks_cli.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
