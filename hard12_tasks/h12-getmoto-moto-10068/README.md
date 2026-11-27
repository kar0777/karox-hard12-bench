# HARD12 task `h12-getmoto-moto-10068`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10068 |
| issue | #9901 (created 2026-03-23) |
| PR created / merged | 2026-06-16 / 2026-06-24 |
| base | `865295ab93afb7324c9768005ffd618bed57ec2b` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 1 / 17 |
| test files | tests/test_transfer/test_transfer.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
