# HARD12 task `h12-open-telemetry-opentelemetry-python-5724`

| item | value |
|---|---|
| source | https://github.com/open-telemetry/opentelemetry-python/pull/5724 |
| issue | #5525 (created 2026-08-07) |
| PR created / merged | 2026-10-02 / 2026-11-19 |
| base | `56eea188789203fc0407ec43d086bb2255f5d784` |
| image base | `swerebench/sweb.eval.x86_64.open-telemetry_1776_opentelemetry-python-4891:latest` |
| F2P / P2P | 6 / 35 |
| test files | opentelemetry-sdk/tests/logs/test_logs.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
