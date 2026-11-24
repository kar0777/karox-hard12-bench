# HARD12 task `h12-agentscope-ai-qwenpaw-8438`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/8438 |
| issue | #8425 (created 2026-10-26) |
| PR created / merged | 2026-10-26 / 2026-10-28 |
| base | `b501aca97f8e13c730669fa1c6365f4f053895b6` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 4 / 120 |
| test files | tests/unit/app/mail/test_driver_config.py, tests/unit/app/mail/test_monitor.py, tests/unit/routers/test_agents_mail_validation.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
