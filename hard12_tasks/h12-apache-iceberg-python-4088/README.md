# HARD12 task `h12-apache-iceberg-python-4088`

| item | value |
|---|---|
| source | https://github.com/apache/iceberg-python/pull/4088 |
| issue | #4073 (created 2026-10-04) |
| PR created / merged | 2026-10-07 / 2026-10-25 |
| base | `12d4a9a3ced73da290626bde6019ac2835d5c636` |
| image base | `swerebench/sweb.eval.x86_64.apache_1776_iceberg-python-3295:latest` |
| F2P / P2P | 3 / 171 |
| test files | tests/catalog/test_rest.py, tests/integration/test_rest_catalog.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
