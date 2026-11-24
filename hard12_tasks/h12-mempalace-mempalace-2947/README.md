# HARD12 task `h12-mempalace-mempalace-2947`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2947 |
| issue | #2945 (created 2026-11-04) |
| PR created / merged | 2026-11-04 / 2026-11-09 |
| base | `38ddf76ca6437f3cea2dc9ee83fc1ac666bc3883` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 7 / 348 |
| test files | tests/test_hooks_cli.py, tests/test_normalize.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
