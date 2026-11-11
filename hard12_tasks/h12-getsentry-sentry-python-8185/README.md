# HARD12 task `h12-getsentry-sentry-python-8185`

| item | value |
|---|---|
| source | https://github.com/getsentry/sentry-python/pull/8185 |
| issue | #8182 (created 2026-11-03) |
| PR created / merged | 2026-11-04 / 2026-11-05 |
| base | `dbc50bd7116ca9f544419749479e5d037f0036df` |
| image base | `swerebench/sweb.eval.x86_64.getsentry_1776_sentry-python-4231:latest` |
| F2P / P2P | 15 / 263 |
| test files | tests/integrations/stdlib/test_httplib.py, tests/test_dsc.py, tests/tracing/test_integration_tests.py, tests/tracing/test_span_streaming.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
