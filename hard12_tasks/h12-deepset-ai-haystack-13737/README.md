# HARD12 task `h12-deepset-ai-haystack-13737`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13737 |
| issue | #13736 (created 2026-11-13) |
| PR created / merged | 2026-11-13 / 2026-11-23 |
| base | `9980b2ae3b5fa13e9560c7620d372a8a737434b6` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 5 / 32 |
| test files | test/hooks/compaction/test_summarization.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
