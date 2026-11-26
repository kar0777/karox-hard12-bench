# HARD12 task `h12-deepset-ai-haystack-12478`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/12478 |
| issue | #12477 (created 2026-08-26) |
| PR created / merged | 2026-08-26 / 2026-08-31 |
| base | `385a561ff1883e0a2f69da20772c26197501823e` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 3 / 40 |
| test files | test/components/preprocessors/test_markdown_header_splitter.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
