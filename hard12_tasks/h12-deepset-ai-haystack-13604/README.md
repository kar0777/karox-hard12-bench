# HARD12 task `h12-deepset-ai-haystack-13604`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13604 |
| issue | #13029 (created 2026-09-30) |
| PR created / merged | 2026-11-06 / 2026-11-11 |
| base | `0ad74747ffd7d9f9b092db97ba2e222080992c2e` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 2 / 59 |
| test files | test/components/retrievers/test_auto_merging_retriever.py, test/components/retrievers/test_auto_merging_retriever_async.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
