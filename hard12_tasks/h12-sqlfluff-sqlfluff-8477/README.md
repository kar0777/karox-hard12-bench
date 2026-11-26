# HARD12 task `h12-sqlfluff-sqlfluff-8477`

| item | value |
|---|---|
| source | https://github.com/sqlfluff/sqlfluff/pull/8477 |
| issue | #6508 (created 2024-12-14) |
| PR created / merged | 2026-09-12 / 2026-09-18 |
| base | `c13f46eda87c410a331aa61a0407a47edf110266` |
| image base | `swerebench/sweb.eval.x86_64.sqlfluff_1776_sqlfluff-7622:latest` |
| F2P / P2P | 13 / 21 |
| test files | test/core/config/loader_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
