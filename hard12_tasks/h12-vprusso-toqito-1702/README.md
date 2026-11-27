# HARD12 task `h12-vprusso-toqito-1702`

| item | value |
|---|---|
| source | https://github.com/vprusso/toqito/pull/1702 |
| issue | #1665 (created 2026-06-29) |
| PR created / merged | 2026-06-30 / 2026-06-30 |
| base | `3162791f7b583ec33d869f0f3e55da1b538841ad` |
| image base | `swerebench/sweb.eval.x86_64.vprusso_1776_toqito-1538:latest` |
| F2P / P2P | 14 / 18 |
| test files | toqito/channel_metrics/tests/test_channel_distinguishability.py, toqito/channel_metrics/tests/test_channel_exclusion.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
