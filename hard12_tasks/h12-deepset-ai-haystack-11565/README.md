# HARD12 task `h12-deepset-ai-haystack-11565`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/11565 |
| issue | #11563 (created 2026-06-09) |
| PR created / merged | 2026-06-09 / 2026-06-11 |
| base | `c1e4e0426817fd86bfcf8c3c55ad8baae8b41ea1` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 6 / 706 |
| test files | test/core/pipeline/test_async_pipeline.py, test/core/pipeline/test_pipeline.py, test/core/test_type_utils.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
