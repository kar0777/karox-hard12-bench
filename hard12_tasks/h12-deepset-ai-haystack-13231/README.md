# HARD12 task `h12-deepset-ai-haystack-13231`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13231 |
| issue | #13230 (created 2026-10-12) |
| PR created / merged | 2026-10-12 / 2026-10-13 |
| base | `6bd30ee0161eb222116bfdddac00856fde5907e0` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 3 / 51 |
| test files | test/components/rankers/test_metafield.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
