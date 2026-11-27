# HARD12 task `h12-pipecat-ai-pipecat-4553`

| item | value |
|---|---|
| source | https://github.com/pipecat-ai/pipecat/pull/4553 |
| issue | #4538 (created 2026-05-21) |
| PR created / merged | 2026-05-23 / 2026-05-27 |
| base | `0c4b8dafc4aaab0954e406b36b1a12804bb32bc4` |
| image base | `swerebench/sweb.eval.x86_64.pipecat-ai_1776_pipecat-4283:latest` |
| F2P / P2P | 1 / 1 |
| test files | tests/test_protobuf_serializer.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
