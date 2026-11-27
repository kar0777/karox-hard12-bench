# HARD12 task `h12-open-telemetry-opentelemetry-python-5364`

| item | value |
|---|---|
| source | https://github.com/open-telemetry/opentelemetry-python/pull/5364 |
| issue | #5358 (created 2026-06-25) |
| PR created / merged | 2026-06-26 / 2026-07-08 |
| base | `322c602c87f38933986a757db918591ade441bd3` |
| image base | `swerebench/sweb.eval.x86_64.open-telemetry_1776_opentelemetry-python-4891:latest` |
| F2P / P2P | 5 / 45 |
| test files | opentelemetry-sdk/tests/resources/test_resources.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
