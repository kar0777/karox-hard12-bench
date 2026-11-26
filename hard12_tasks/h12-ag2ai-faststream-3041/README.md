# HARD12 task `h12-ag2ai-faststream-3041`

| item | value |
|---|---|
| source | https://github.com/ag2ai/faststream/pull/3041 |
| issue | #3035 (created 2026-08-22) |
| PR created / merged | 2026-08-25 / 2026-08-27 |
| base | `4090383d5ffa65ec8e3f98ebe8120412af354ab2` |
| image base | `swerebench/sweb.eval.x86_64.ag2ai_1776_faststream-2701:latest` |
| F2P / P2P | 2 / 25 |
| test files | tests/asyncapi/nats/v3_0_0/test_naming.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
