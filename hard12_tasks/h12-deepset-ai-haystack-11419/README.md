# HARD12 task `h12-deepset-ai-haystack-11419`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/11419 |
| issue | #11418 (created 2026-05-27) |
| PR created / merged | 2026-05-27 / 2026-05-29 |
| base | `c3b049b8e4b77384cba5029972e32667846e34ed` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 1 / 7 |
| test files | test/components/classifiers/test_document_language_classifier.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
