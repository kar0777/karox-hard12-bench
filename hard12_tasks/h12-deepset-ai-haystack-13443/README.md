# HARD12 task `h12-deepset-ai-haystack-13443`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13443 |
| issue | #13438 (created 2026-10-26) |
| PR created / merged | 2026-10-26 / 2026-10-26 |
| base | `61f8772ad6d8f548fd7809fa2a1328dc6d3b15eb` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 11 / 99 |
| test files | test/components/agents/test_agent_hitl.py, test/components/generators/chat/test_openai.py, test/components/generators/chat/test_openai_responses.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
