# HARD12 task `h12-open-telemetry-opentelemetry-python-5336`

| item | value |
|---|---|
| source | https://github.com/open-telemetry/opentelemetry-python/pull/5336 |
| issue | #5330 (created 2026-06-19) |
| PR created / merged | 2026-06-19 / 2026-06-25 |
| base | `0e542338285931e2a45e904f55df1681e2658828` |
| image base | `swerebench/sweb.eval.x86_64.open-telemetry_1776_opentelemetry-python-4891:latest` |
| F2P / P2P | 15 / 25 |
| test files | opentelemetry-sdk/tests/metrics/integration_test/test_nonfinite_measurements.py, opentelemetry-sdk/tests/metrics/test_instrument.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
