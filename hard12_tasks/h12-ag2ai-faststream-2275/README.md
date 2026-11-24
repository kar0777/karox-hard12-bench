# HARD12 task `h12-ag2ai-faststream-2275`

| item | value |
|---|---|
| source | https://github.com/ag2ai/faststream/pull/2275 |
| issue | #2220 (created 2025-05-20) |
| PR created / merged | 2025-06-09 / 2026-10-24 |
| base | `05f2a5951944e471bbcf6ca324cbd2ff4421eafe` |
| image base | `swerebench/sweb.eval.x86_64.ag2ai_1776_faststream-2701:latest` |
| F2P / P2P | 2 / 0 |
| test files | tests/docs/getting_started/prometheus/test_kafka_multiprocess.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
