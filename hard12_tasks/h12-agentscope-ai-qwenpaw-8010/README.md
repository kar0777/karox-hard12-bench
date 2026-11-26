# HARD12 task `h12-agentscope-ai-qwenpaw-8010`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/8010 |
| issue | #8009 (created 2026-09-28) |
| PR created / merged | 2026-09-28 / 2026-10-09 |
| base | `70715e982ee66f883afa707e29a741ac6aed26d6` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 2 / 14 |
| test files | tests/unit/agents/test_react_agent_media_strip.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
