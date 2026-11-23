# HARD12 task `h12-agentscope-ai-qwenpaw-8734`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/8734 |
| issue | #8733 (created 2026-11-14) |
| PR created / merged | 2026-11-14 / 2026-11-17 |
| base | `f47dd19bd1442b989eeb8df8d146cbbab572d0b1` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 1 / 0 |
| test files | tests/unit/plugins/test_legacy_cloudpaw_compat.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
