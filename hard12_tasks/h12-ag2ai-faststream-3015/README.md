# HARD12 task `h12-ag2ai-faststream-3015`

| item | value |
|---|---|
| source | https://github.com/ag2ai/faststream/pull/3015 |
| issue | #3013 (created 2026-08-12) |
| PR created / merged | 2026-08-13 / 2026-08-13 |
| base | `83fab8807f619944cd87c0cd522e132777fd55a2` |
| image base | `swerebench/sweb.eval.x86_64.ag2ai_1776_faststream-2701:latest` |
| F2P / P2P | 1 / 16 |
| test files | tests/brokers/redis/test_config.py, tests/brokers/redis/test_consume.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
