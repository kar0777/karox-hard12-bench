# HARD12 task `h12-databricks-dbt-databricks-1610`

| item | value |
|---|---|
| source | https://github.com/databricks/dbt-databricks/pull/1610 |
| issue | #1609 (created 2026-07-27) |
| PR created / merged | 2026-07-27 / 2026-08-09 |
| base | `006d0c231fc3cd2a09b69e0d1e2bf298e681f0cf` |
| image base | `swerebench/sweb.eval.x86_64.databricks_1776_dbt-databricks-1428:latest` |
| F2P / P2P | 25 / 0 |
| test files | tests/unit/test_utils.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
