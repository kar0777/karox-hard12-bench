# HARD12 task `h12-deepset-ai-haystack-11493`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/11493 |
| issue | #11453 (created 2026-06-01) |
| PR created / merged | 2026-06-03 / 2026-06-18 |
| base | `ed472f040f93fa87d286009092b6dbd6a21c23f1` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 1 / 7 |
| test files | test/core/component/test_sockets.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
