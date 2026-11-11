# HARD12 task `h12-databricks-dbt-databricks-1749`

| item | value |
|---|---|
| source | https://github.com/databricks/dbt-databricks/pull/1749 |
| issue | #1748 (created 2026-10-27) |
| PR created / merged | 2026-10-27 / 2026-11-02 |
| base | `8e63d2be4b2ea96e196c714ec70eac3023294458` |
| image base | `swerebench/sweb.eval.x86_64.databricks_1776_dbt-databricks-1428:latest` |
| F2P / P2P | 1 / 117 |
| test files | tests/unit/test_adapter.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
