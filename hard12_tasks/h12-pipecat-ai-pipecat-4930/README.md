# HARD12 task `h12-pipecat-ai-pipecat-4930`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/4930 |
| issue | #4831 (created 2026-06-19) |
| PR created / merged | 2026-07-01 / 2026-07-01 |
| base | `b43d91caa69e7001621236af1609978552711085` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 1 / 78 |
| test files | tests/test_aggregated_frame_sequencer.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
