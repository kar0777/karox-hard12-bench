# HARD12 task `h12-deepset-ai-haystack-13424`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13424 |
| issue | #13423 (created 2026-10-24) |
| PR created / merged | 2026-10-24 / 2026-11-16 |
| base | `622967d7b6a878085a72ce9fb942bab0f485ad2f` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 2 / 16 |
| test files | test/components/evaluators/test_faithfulness_evaluator.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
