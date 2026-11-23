# HARD12 task `h12-getmoto-moto-10297`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10297 |
| issue | #10176 (created 2026-08-11) |
| PR created / merged | 2026-09-29 / 2026-11-15 |
| base | `c5f05794a3d779ee6a781d3b1a858911d64484c4` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 10 / 152 |
| test files | tests/test_dynamodb/test_dynamodb.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
