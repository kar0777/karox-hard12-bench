# HARD12 task `h12-pipecat-ai-pipecat-4482`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/4482 |
| issue | #4476 (created 2026-05-13) |
| PR created / merged | 2026-05-13 / 2026-05-13 |
| base | `08680732f61a2b238064f06b8337c9b48a7459ce` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 7 / 0 |
| test files | tests/test_soniox_stt.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
