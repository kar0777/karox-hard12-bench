# HARD12 task `h12-deepset-ai-haystack-12685`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/12685 |
| issue | #12684 (created 2026-09-10) |
| PR created / merged | 2026-09-10 / 2026-09-10 |
| base | `3f83fa9a54be77f7666dfc122962be6c5d934945` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 2 / 28 |
| test files | test/components/extractors/test_llm_metadata_extractor.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
