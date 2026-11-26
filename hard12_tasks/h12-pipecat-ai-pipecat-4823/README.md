# HARD12 task `h12-pipecat-ai-pipecat-4823`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/4823 |
| issue | #4822 (created 2026-06-19) |
| PR created / merged | 2026-06-19 / 2026-09-23 |
| base | `5a66933690efa8ca308b621282592fb09fcb6c6a` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 2 / 52 |
| test files | tests/test_auto_register_tools.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
