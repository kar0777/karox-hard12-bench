# HARD12 task `h12-getmoto-moto-10175`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10175 |
| issue | #10174 (created 2026-08-10) |
| PR created / merged | 2026-08-11 / 2026-08-11 |
| base | `7dc0838503a3da50ac83980dc82c07572bb5212a` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 17 / 0 |
| test files | tests/test_dynamodb/__init__.py, tests/test_dynamodb/test_dynamodb_select.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
