# HARD12 task `h12-pipecat-ai-pipecat-6411`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/6411 |
| issue | #6410 (created 2026-10-27) |
| PR created / merged | 2026-10-27 / 2026-10-28 |
| base | `a2cb3d60205f7555e2affe54e729ccd918360f8d` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 1 / 4 |
| test files | tests/test_time_utils.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
