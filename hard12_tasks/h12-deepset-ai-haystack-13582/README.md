# HARD12 task `h12-deepset-ai-haystack-13582`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13582 |
| issue | #13581 (created 2026-11-06) |
| PR created / merged | 2026-11-06 / 2026-11-10 |
| base | `ddcde93b1f1d9e05c5a0c286da8f1ce16d59e6c7` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 6 / 59 |
| test files | test/components/joiners/test_document_joiner.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
