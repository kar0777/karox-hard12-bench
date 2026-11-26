# HARD12 task `h12-pipecat-ai-pipecat-5205`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/5205 |
| issue | #5204 (created 2026-08-03) |
| PR created / merged | 2026-08-03 / 2026-08-03 |
| base | `b114a367a32166207712e8a9c352215a6e24a0db` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 1 / 76 |
| test files | tests/test_voice_formatting.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
