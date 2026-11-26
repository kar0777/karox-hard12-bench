# HARD12 task `h12-terrapower-armi-2607`

| item | value |
|---|---|
| source | https://github.com/terrapower/armi/pull/2607 |
| issue | #1960 (created 2024-10-18) |
| PR created / merged | 2026-07-27 / 2026-07-30 |
| base | `3032f9047c316ee12c823a1ec8990aaece487767` |
| image base | `swerebench/sweb.eval.x86_64.terrapower_1776_armi-2285:latest` |
| F2P / P2P | 1 / 28 |
| test files | armi/bookkeeping/db/tests/test_database.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
