# HARD12 task `h12-ag2ai-faststream-2876`

| item | value |
|---|---|
| source | https://github.com/ag2ai/faststream/pull/2876 |
| issue | #2869 (created 2026-05-14) |
| PR created / merged | 2026-05-18 / 2026-05-25 |
| base | `6a4ccfd15c8a339003d0d7357b154a61a51cf48b` |
| image base | `swerebench/sweb.eval.x86_64.ag2ai_1776_faststream-2701:latest` |
| F2P / P2P | 2 / 3 |
| test files | tests/asyncapi/test_fastapi_router.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
