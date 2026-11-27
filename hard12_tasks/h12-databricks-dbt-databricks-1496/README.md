# HARD12 task `h12-databricks-dbt-databricks-1496`

| item | value |
|---|---|
| source | https://github.com/databricks/dbt-databricks/pull/1496 |
| issue | #1495 (created 2026-06-03) |
| PR created / merged | 2026-06-04 / 2026-06-05 |
| base | `0263f4a539a5bd658fa8f8eb66cede53b573fbed` |
| image base | `swerebench/sweb.eval.x86_64.databricks_1776_dbt-databricks-1428:latest` |
| F2P / P2P | 3 / 7 |
| test files | tests/functional/adapter/iceberg/fixtures.py, tests/functional/adapter/iceberg/test_iceberg_support.py, tests/unit/relation_configs/test_liquid_clustering.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
