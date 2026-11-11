# HARD12 task `h12-deepset-ai-haystack-13615`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13615 |
| issue | #13554 (created 2026-11-04) |
| PR created / merged | 2026-11-07 / 2026-11-09 |
| base | `d35db5a1f48d0abfc4bd508470b7e00eb1376a0c` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 4 / 35 |
| test files | test/components/builders/test_answer_builder.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
