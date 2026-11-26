# HARD12 task `h12-vprusso-toqito-1891`

| item | value |
|---|---|
| source | https://github.com/vprusso/toqito/pull/1891 |
| issue | #1885 (created 2026-07-25) |
| PR created / merged | 2026-07-25 / 2026-07-27 |
| base | `c35a4b2a10b6fc8188540b93d67b5b9c9e7ab092` |
| image base | `swerebench/sweb.eval.x86_64.vprusso_1776_toqito-1538:latest` |
| F2P / P2P | 1 / 8 |
| test files | toqito/channel_metrics/tests/test_completely_bounded_trace_norm.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
