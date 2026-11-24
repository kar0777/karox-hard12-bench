# HARD12 task `h12-mempalace-mempalace-2625`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2625 |
| issue | #2614 (created 2026-09-28) |
| PR created / merged | 2026-09-29 / 2026-11-08 |
| base | `785521606a98a406f77bd22754d798523efc9f6c` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 14 / 103 |
| test files | tests/test_hub_forward.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
