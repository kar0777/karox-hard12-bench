# HARD12 task `h12-deepset-ai-haystack-13189`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13189 |
| issue | #13188 (created 2026-10-08) |
| PR created / merged | 2026-10-08 / 2026-10-12 |
| base | `16de9eef895755a693ee51d1f6a92369722cc85e` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 1 / 65 |
| test files | test/test_logging.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
