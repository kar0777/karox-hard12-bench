# HARD12 task `h12-open-telemetry-opentelemetry-python-5650`

| item | value |
|---|---|
| source | https://github.com/open-telemetry/opentelemetry-python/pull/5650 |
| issue | #5648 (created 2026-09-10) |
| PR created / merged | 2026-09-10 / 2026-10-26 |
| base | `c8928f735f88b6fda75d870c9da508a347dab368` |
| image base | `swerebench/sweb.eval.x86_64.open-telemetry_1776_opentelemetry-python-4891:latest` |
| F2P / P2P | 2 / 42 |
| test files | opentelemetry-sdk/tests/logs/test_export.py, opentelemetry-sdk/tests/trace/export/test_export.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
