# HARD12 task `h12-deepset-ai-haystack-12303`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/12303 |
| issue | #12300 (created 2026-08-11) |
| PR created / merged | 2026-08-11 / 2026-08-24 |
| base | `66c3fd870cd0ef2d24ce656ba82aea84a12e76a0` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 8 / 118 |
| test files | test/components/agents/test_agent.py, test/components/generators/chat/test_openai_responses_conversion.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
