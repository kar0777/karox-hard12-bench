# HARD12 task `h12-deepset-ai-haystack-12059`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/12059 |
| issue | #12058 (created 2026-07-17) |
| PR created / merged | 2026-07-17 / 2026-07-21 |
| base | `007c66bf712c8f4ab45a08f16c99e7804039e462` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 3 / 7 |
| test files | test/hooks/tool_result_offloading/test_stores.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
