# HARD12 task `h12-sqlfluff-sqlfluff-8271`

| item | value |
|---|---|
| source | https://github.com/sqlfluff/sqlfluff/pull/8271 |
| issue | #4237 (created 2023-01-03) |
| PR created / merged | 2026-08-01 / 2026-08-12 |
| base | `d19152f9ecb69dbc7cd018e4dd8d90e454efcfed` |
| image base | `swerebench/sweb.eval.x86_64.sqlfluff_1776_sqlfluff-7622:latest` |
| F2P / P2P | 10 / 80 |
| test files | test/core/config/fluffconfig_test.py, test/core/config/validate_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
