# HARD12 task `h12-ag2ai-faststream-2951`

| item | value |
|---|---|
| source | https://github.com/ag2ai/faststream/pull/2951 |
| issue | #2943 (created 2026-07-19) |
| PR created / merged | 2026-07-24 / 2026-07-29 |
| base | `8a4ce176966ab14e559f52b039e3e16795831b7a` |
| image base | `swerebench/sweb.eval.x86_64.ag2ai_1776_faststream-2701:latest` |
| F2P / P2P | 16 / 4 |
| test files | tests/brokers/confluent/test_batch_body.py, tests/brokers/kafka/test_batch_body.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
