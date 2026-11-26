# HARD12 task `h12-deepset-ai-haystack-12907`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/12907 |
| issue | #12906 (created 2026-09-24) |
| PR created / merged | 2026-09-24 / 2026-09-30 |
| base | `43547276ad4fa8a4fc16181275541d78e8c64767` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 5 / 75 |
| test files | test/components/builders/test_chat_prompt_builder.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
