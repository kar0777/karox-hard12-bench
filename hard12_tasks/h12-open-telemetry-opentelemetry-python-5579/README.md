# HARD12 task `h12-open-telemetry-opentelemetry-python-5579`

| item | value |
|---|---|
| source | https://github.com/open-telemetry/opentelemetry-python/pull/5579 |
| issue | #5578 (created 2026-08-23) |
| PR created / merged | 2026-08-23 / 2026-11-06 |
| base | `ba48fefdb9ae9bb613c431c21625fe55cdef1bca` |
| image base | `swerebench/sweb.eval.x86_64.open-telemetry_1776_opentelemetry-python-4891:latest` |
| F2P / P2P | 25 / 20 |
| test files | opentelemetry-sdk/tests/trace/composite_sampler/test_parent_threshold.py, opentelemetry-sdk/tests/trace/composite_sampler/test_propagation.py, opentelemetry-sdk/tests/trace/composite_sampler/test_sampler.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
