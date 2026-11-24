# HARD12 task `h12-deepset-ai-haystack-13344`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13344 |
| issue | #12954 (created 2026-09-25) |
| PR created / merged | 2026-10-20 / 2026-10-21 |
| base | `c61e146f3577116f5a1e546192b3c69e882a7838` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 4 / 70 |
| test files | test/components/preprocessors/test_markdown_header_splitter.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
