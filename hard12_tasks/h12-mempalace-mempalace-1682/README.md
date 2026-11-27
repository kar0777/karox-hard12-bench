# HARD12 task `h12-mempalace-mempalace-1682`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/1682 |
| issue | #1681 (created 2026-06-03) |
| PR created / merged | 2026-06-03 / 2026-06-06 |
| base | `02b8753d9759e7c17eca58ba5162e5d2a39ca3d2` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 7 / 97 |
| test files | tests/test_miner.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
