# HARD12 task `h12-pipecat-ai-pipecat-5642`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/5642 |
| issue | #5504 (created 2026-08-31) |
| PR created / merged | 2026-09-05 / 2026-09-06 |
| base | `833b382155713d69f13c5cd9227678e148c2b4e3` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 2 / 20 |
| test files | tests/test_llm_context_summarizer.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
