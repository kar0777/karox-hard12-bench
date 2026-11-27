# HARD12 task `h12-ag2ai-faststream-2859`

| item | value |
|---|---|
| source | https://github.com/ag2ai/faststream/pull/2859 |
| issue | #2691 (created 2025-11-24) |
| PR created / merged | 2026-05-07 / 2026-05-13 |
| base | `3464351eb17424c85551cf9b4e0225f3afc53b1e` |
| image base | `swerebench/sweb.eval.x86_64.ag2ai_1776_faststream-2701:latest` |
| F2P / P2P | 2 / 0 |
| test files | tests/brokers/confluent/test_lazy_logger_proxy.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
