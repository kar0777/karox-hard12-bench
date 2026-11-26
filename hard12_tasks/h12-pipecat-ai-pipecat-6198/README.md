# HARD12 task `h12-pipecat-ai-pipecat-6198`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/6198 |
| issue | #6185 (created 2026-10-15) |
| PR created / merged | 2026-10-16 / 2026-10-16 |
| base | `f7c191f743807dc9380d8201f387d6767f544a07` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 6 / 4 |
| test files | tests/test_anthropic_stop_reason.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
