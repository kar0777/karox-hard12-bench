# HARD12 task `h12-beeware-briefcase-3086`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/3086 |
| issue | #3075 (created 2026-10-01) |
| PR created / merged | 2026-10-07 / 2026-10-12 |
| base | `69a4bab94380497c4598c7b44fcaf094420378c2` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 6 / 51 |
| test files | tests/platforms/windows/app/create/test_create.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
