# HARD12 task `h12-pipecat-ai-pipecat-5108`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/5108 |
| issue | #4611 (created 2026-06-01) |
| PR created / merged | 2026-07-23 / 2026-07-24 |
| base | `8e4e1dc707dff2ec8b4b246bae881934ac7b2a17` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 1 / 33 |
| test files | tests/test_tts_frame_ordering.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
