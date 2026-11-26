# HARD12 task `h12-getmoto-moto-10248`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10248 |
| issue | #10247 (created 2026-09-08) |
| PR created / merged | 2026-09-08 / 2026-09-12 |
| base | `f1c997b3bc3ec2ec71b3ab3b53df102a447a1f38` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 5 / 13 |
| test files | tests/test_kafka/test_kafka.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
