# HARD12 task `h12-pipecat-ai-pipecat-4887`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/4887 |
| issue | #4870 (created 2026-06-24) |
| PR created / merged | 2026-06-25 / 2026-06-26 |
| base | `1e56858c5f3521eac2d5430ae294e7e8f963c573` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 2 / 39 |
| test files | tests/test_evals_scenario.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
