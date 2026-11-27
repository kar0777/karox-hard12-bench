# HARD12 task `h12-open-telemetry-opentelemetry-python-5179`

| item | value |
|---|---|
| source | https://github.com/open-telemetry/opentelemetry-python/pull/5179 |
| issue | #4631 (created 2025-06-11) |
| PR created / merged | 2026-05-05 / 2026-05-11 |
| base | `86d9bae0469d693159a8db783711354722d390c2` |
| image base | `swerebench/sweb.eval.x86_64.open-telemetry_1776_opentelemetry-python-4891:latest` |
| F2P / P2P | 7 / 31 |
| test files | opentelemetry-sdk/tests/logs/test_multi_log_processor.py, opentelemetry-sdk/tests/trace/test_span_processor.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
