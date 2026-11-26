# HARD12 task `h12-agentscope-ai-qwenpaw-6180`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/6180 |
| issue | #6131 (created 2026-07-15) |
| PR created / merged | 2026-07-16 / 2026-07-16 |
| base | `f9c3f2d29cf59f247cc37725798a50af885f3493` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 1 / 0 |
| test files | tests/integration/test_console_chat_updated_at.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
