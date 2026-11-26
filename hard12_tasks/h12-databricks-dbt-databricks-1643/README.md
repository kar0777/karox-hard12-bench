# HARD12 task `h12-databricks-dbt-databricks-1643`

| item | value |
|---|---|
| source | https://github.com/databricks/dbt-databricks/pull/1643 |
| issue | #1641 (created 2026-08-14) |
| PR created / merged | 2026-08-19 / 2026-08-21 |
| base | `4d2d6141238aed661999ac28ab5d6e0ae18908fb` |
| image base | `swerebench/sweb.eval.x86_64.databricks_1776_dbt-databricks-1428:latest` |
| F2P / P2P | 3 / 124 |
| test files | tests/functional/adapter/incremental/fixtures.py, tests/functional/adapter/incremental/test_incremental_metadata_fetch_skips.py, tests/unit/record/test_record_types.py, tests/unit/relation_configs/test_constraint.py, tests/unit/test_adapter.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
