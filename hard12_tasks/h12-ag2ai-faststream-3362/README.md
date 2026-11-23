# HARD12 task `h12-ag2ai-faststream-3362`

| item | value |
|---|---|
| source | https://github.com/ag2ai/faststream/pull/3362 |
| issue | #3343 (created 2026-11-16) |
| PR created / merged | 2026-11-16 / 2026-11-17 |
| base | `4047adcc2d40605d4ddb458094c9b89e79ae4da1` |
| image base | `swerebench/sweb.eval.x86_64.ag2ai_1776_faststream-2701:latest` |
| F2P / P2P | 3 / 10 |
| test files | tests/brokers/redis/test_parser.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
