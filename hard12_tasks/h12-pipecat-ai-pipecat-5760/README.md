# HARD12 task `h12-pipecat-ai-pipecat-5760`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/5760 |
| issue | #5481 (created 2026-08-28) |
| PR created / merged | 2026-09-14 / 2026-09-15 |
| base | `f6d601303de62926a476c2a97675e39f37d92854` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 1 / 67 |
| test files | tests/test_llm_service.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
