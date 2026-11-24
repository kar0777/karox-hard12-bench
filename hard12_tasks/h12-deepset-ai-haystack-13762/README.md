# HARD12 task `h12-deepset-ai-haystack-13762`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13762 |
| issue | #13740 (created 2026-11-13) |
| PR created / merged | 2026-11-16 / 2026-11-23 |
| base | `4b4346b6d798338d9b43e70115006494012b1756` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 9 / 91 |
| test files | test/components/preprocessors/test_document_splitter.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
