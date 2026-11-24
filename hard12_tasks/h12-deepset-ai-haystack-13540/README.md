# HARD12 task `h12-deepset-ai-haystack-13540`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13540 |
| issue | #13487 (created 2026-10-30) |
| PR created / merged | 2026-11-03 / 2026-11-03 |
| base | `b8d27b4f4b378a178ed1e4ba67a59bc1998ef1ee` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 1 / 25 |
| test files | test/components/generators/chat/test_llm.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
