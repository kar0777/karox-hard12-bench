# HARD12 task `h12-mempalace-mempalace-2943`

| item | value |
|---|---|
| source | https://github.com/MemPalace/mempalace/pull/2943 |
| issue | #2917 (created 2026-10-31) |
| PR created / merged | 2026-11-04 / 2026-11-08 |
| base | `2da78c883a61a2fa689103c65a1fa9cab18d4dc3` |
| image base | `swerebench/sweb.eval.x86_64.mempalace_1776_mempalace-1004:latest` |
| F2P / P2P | 11 / 57 |
| test files | tests/test_convo_miner.py, tests/test_hook_mine_shutdown.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
