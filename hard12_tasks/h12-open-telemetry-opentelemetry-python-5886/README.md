# HARD12 task `h12-open-telemetry-opentelemetry-python-5886`

| item | value |
|---|---|
| source | https://github.com/open-telemetry/opentelemetry-python/pull/5886 |
| issue | #5877 (created 2026-11-01) |
| PR created / merged | 2026-11-06 / 2026-11-10 |
| base | `2b1246ed8dc4d409751b75b685db3b2cf064b2b7` |
| image base | `swerebench/sweb.eval.x86_64.open-telemetry_1776_opentelemetry-python-4891:latest` |
| F2P / P2P | 12 / 0 |
| test files | opentelemetry-api/tests/test_sdk_backcompat.py, opentelemetry-api/tests/util/test_compat.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
