# HARD12 task `h12-databricks-dbt-databricks-1728`

| item | value |
|---|---|
| source | https://github.com/databricks/dbt-databricks/pull/1728 |
| issue | #1724 (created 2026-10-15) |
| PR created / merged | 2026-10-16 / 2026-11-02 |
| base | `c4cc9c5480720632bea4c71bc5b3ab031a3ff0c4` |
| image base | `swerebench/sweb.eval.x86_64.databricks_1776_dbt-databricks-1428:latest` |
| F2P / P2P | 5 / 6 |
| test files | tests/unit/test_credentials_connection_info.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
