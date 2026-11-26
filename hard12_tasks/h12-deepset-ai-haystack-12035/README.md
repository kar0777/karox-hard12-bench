# HARD12 task `h12-deepset-ai-haystack-12035`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/12035 |
| issue | #12022 (created 2026-07-15) |
| PR created / merged | 2026-07-16 / 2026-07-20 |
| base | `5d101e5a8029496c53a7c5ca3c5fa72a7813be79` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 4 / 43 |
| test files | test/components/query/test_query_expander.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
