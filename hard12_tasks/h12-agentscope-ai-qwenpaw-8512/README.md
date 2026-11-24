# HARD12 task `h12-agentscope-ai-qwenpaw-8512`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/8512 |
| issue | #8505 (created 2026-10-30) |
| PR created / merged | 2026-10-30 / 2026-11-20 |
| base | `8aac2ad8c54169326ff37326fff851de7c6192e3` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 3 / 37 |
| test files | tests/unit/providers/test_model_error_policy.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
