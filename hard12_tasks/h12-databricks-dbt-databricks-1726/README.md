# HARD12 task `h12-databricks-dbt-databricks-1726`

| item | value |
|---|---|
| source | https://github.com/databricks/dbt-databricks/pull/1726 |
| issue | #1380 (created 2026-04-02) |
| PR created / merged | 2026-10-15 / 2026-11-02 |
| base | `3d060e2d4bb35596615c16628896497e61b6f858` |
| image base | `swerebench/sweb.eval.x86_64.databricks_1776_dbt-databricks-1428:latest` |
| F2P / P2P | 14 / 47 |
| test files | tests/functional/adapter/columns/fixtures.py, tests/functional/adapter/columns/test_get_columns.py, tests/unit/test_column.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
