# HARD12 task `h12-mempalace-mempalace-2564`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2564 |
| issue | #2563 (created 2026-09-21) |
| PR created / merged | 2026-09-21 / 2026-09-21 |
| base | `e038af9703d2467bb7cfffdd3f7fb2bd212e58a4` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 10 / 101 |
| test files | tests/test_sync.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
