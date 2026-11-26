# HARD12 task `h12-agentscope-ai-qwenpaw-7636`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/7636 |
| issue | #7597 (created 2026-09-07) |
| PR created / merged | 2026-09-08 / 2026-09-16 |
| base | `107eb7f7e2911ad90e13b6d5ff62c513013bc363` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 32 / 0 |
| test files | tests/unit/agents/test_message_request_normalizer.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
