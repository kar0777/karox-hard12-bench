# HARD12 task `h12-mempalace-mempalace-2699`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2699 |
| issue | #2676 (created 2026-10-05) |
| PR created / merged | 2026-10-07 / 2026-10-10 |
| base | `d439d1e6d01e2680d79fe3f5de5a336722cec779` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 9 / 140 |
| test files | tests/test_miner.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
