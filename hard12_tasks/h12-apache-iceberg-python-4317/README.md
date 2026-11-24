# HARD12 task `h12-apache-iceberg-python-4317`

| item | value |
|---|---|
| source | https://github.com/apache/iceberg-python/pull/4317 |
| issue | #4316 (created 2026-11-09) |
| PR created / merged | 2026-11-09 / 2026-11-11 |
| base | `639a3bf505b6932945bba3f661395255bac872c2` |
| image base | `swerebench/sweb.eval.x86_64.apache_1776_iceberg-python-3295:latest` |
| F2P / P2P | 6 / 132 |
| test files | tests/table/test_commit_retry.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
