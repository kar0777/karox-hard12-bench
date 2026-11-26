# HARD12 task `h12-databricks-dbt-databricks-1720`

| item | value |
|---|---|
| source | https://github.com/databricks/dbt-databricks/pull/1720 |
| issue | #1356 (created 2026-03-13) |
| PR created / merged | 2026-10-14 / 2026-10-19 |
| base | `c1add903c70819b61b512027c33871a7857dadff` |
| image base | `swerebench/sweb.eval.x86_64.databricks_1776_dbt-databricks-1428:latest` |
| F2P / P2P | 3 / 16 |
| test files | tests/functional/adapter/views/fixtures.py, tests/functional/adapter/views/test_view_metadata_fetch_skips.py, tests/functional/adapter/views/test_views.py, tests/unit/relation_configs/test_query.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
