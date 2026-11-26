# HARD12 task `h12-mempalace-mempalace-2499`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2499 |
| issue | #2498 (created 2026-09-14) |
| PR created / merged | 2026-09-14 / 2026-09-15 |
| base | `38260df588968604186b525ecdffb41c140e5f61` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 7 / 205 |
| test files | tests/test_non_regular_file_guards.py, tests/test_repair.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
