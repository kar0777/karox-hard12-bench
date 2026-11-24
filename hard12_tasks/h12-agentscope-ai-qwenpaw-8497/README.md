# HARD12 task `h12-agentscope-ai-qwenpaw-8497`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/8497 |
| issue | #8265 (created 2026-10-15) |
| PR created / merged | 2026-10-29 / 2026-10-29 |
| base | `314a59166a40f88667bc68c8ef10f37dd009f1cf` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 2 / 1 |
| test files | tests/unit/plugins/test_plugin_namespace_isolation.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
