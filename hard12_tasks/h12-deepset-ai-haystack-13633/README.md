# HARD12 task `h12-deepset-ai-haystack-13633`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13633 |
| issue | #13631 (created 2026-11-09) |
| PR created / merged | 2026-11-09 / 2026-11-10 |
| base | `8872d2bfba932964638c26575b074184913a8074` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 2 / 65 |
| test files | test/tools/test_searchable_toolset.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
