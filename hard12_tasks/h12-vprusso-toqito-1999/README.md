# HARD12 task `h12-vprusso-toqito-1999`

| item | value |
|---|---|
| source | https://github.com/vprusso/toqito/pull/1999 |
| issue | #1988 (created 2026-10-18) |
| PR created / merged | 2026-10-28 / 2026-11-03 |
| base | `7e0b1a0f7f780215fbe8f6b1f18e1577bf8cfa65` |
| image base | `swerebench/sweb.eval.x86_64.vprusso_1776_toqito-1538:latest` |
| F2P / P2P | 5 / 6 |
| test files | toqito/state_metrics/tests/test_measured_relative_entropy.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
