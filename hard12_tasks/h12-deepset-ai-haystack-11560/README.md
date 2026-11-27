# HARD12 task `h12-deepset-ai-haystack-11560`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/11560 |
| issue | #11559 (created 2026-06-09) |
| PR created / merged | 2026-06-09 / 2026-06-09 |
| base | `12d6f687d5da4cf19df36341b9cbcae75e43e88b` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 5 / 12 |
| test files | test/components/generators/chat/test_azure.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
