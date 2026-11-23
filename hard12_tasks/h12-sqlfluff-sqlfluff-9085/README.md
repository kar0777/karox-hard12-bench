# HARD12 task `h12-sqlfluff-sqlfluff-9085`

| item | value |
|---|---|
| source | https://github.com/sqlfluff/sqlfluff/pull/9085 |
| issue | #9005 (created 2026-11-04) |
| PR created / merged | 2026-11-09 / 2026-11-15 |
| base | `2ce9773271a0629913f268bd15aa47f9ea61c40f` |
| image base | `swerebench/sweb.eval.x86_64.sqlfluff_1776_sqlfluff-7622:latest` |
| F2P / P2P | 5 / 74 |
| test files | test/core/rules/noqa_test.py, test/core/rules/rules_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
