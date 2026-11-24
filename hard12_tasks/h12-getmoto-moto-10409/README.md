# HARD12 task `h12-getmoto-moto-10409`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10409 |
| issue | #10404 (created 2026-10-19) |
| PR created / merged | 2026-10-19 / 2026-10-27 |
| base | `dd8bf40ded62c303019c5d5e9027ffd3ed6f1628` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 1 / 158 |
| test files | tests/test_sqs/test_sqs.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
