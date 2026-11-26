# HARD12 task `h12-agentscope-ai-qwenpaw-6183`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/6183 |
| issue | #6178 (created 2026-07-16) |
| PR created / merged | 2026-07-16 / 2026-07-21 |
| base | `f420b677d73c6b18530ac9c9cc3dbb75008743a1` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 33 / 0 |
| test files | tests/unit/utils/test_logging.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
