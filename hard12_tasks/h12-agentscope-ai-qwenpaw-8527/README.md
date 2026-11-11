# HARD12 task `h12-agentscope-ai-qwenpaw-8527`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/8527 |
| issue | #8515 (created 2026-10-31) |
| PR created / merged | 2026-11-01 / 2026-11-04 |
| base | `c26d31c0688aa9cce9bc1aef688177d2e14e25df` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 2 / 22 |
| test files | tests/unit/plugins/test_install_lock.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
