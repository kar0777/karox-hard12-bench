# HARD12 task `h12-databricks-dbt-databricks-1526`

| item | value |
|---|---|
| source | https://github.com/databricks/dbt-databricks/pull/1526 |
| issue | #1525 (created 2026-06-16) |
| PR created / merged | 2026-06-16 / 2026-06-23 |
| base | `fdbee5b89b800ab929130733512e03070e326e7e` |
| image base | `swerebench/sweb.eval.x86_64.databricks_1776_dbt-databricks-1428:latest` |
| F2P / P2P | 3 / 89 |
| test files | tests/functional/adapter/column_tags/test_column_tags.py, tests/unit/macros/relations/test_view_macros.py, tests/unit/test_adapter.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
