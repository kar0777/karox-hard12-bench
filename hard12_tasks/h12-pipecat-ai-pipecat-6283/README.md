# HARD12 task `h12-pipecat-ai-pipecat-6283`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/6283 |
| issue | #6272 (created 2026-10-20) |
| PR created / merged | 2026-10-21 / 2026-10-21 |
| base | `32d63cb97de2bb2ecc732d0427ac1fb4e0c7e8c6` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 1 / 25 |
| test files | tests/test_redaction.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
