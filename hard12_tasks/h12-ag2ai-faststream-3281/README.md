# HARD12 task `h12-ag2ai-faststream-3281`

| item | value |
|---|---|
| source | https://github.com/ag2ai/faststream/pull/3281 |
| issue | #3280 (created 2026-10-22) |
| PR created / merged | 2026-10-22 / 2026-10-22 |
| base | `600a353764753c2427c60d2aad278ecb08be90f5` |
| image base | `swerebench/sweb.eval.x86_64.ag2ai_1776_faststream-2701:latest` |
| F2P / P2P | 2 / 2 |
| test files | tests/brokers/confluent/test_message.py, tests/brokers/kafka/test_message.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
