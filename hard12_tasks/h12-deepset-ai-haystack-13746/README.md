# HARD12 task `h12-deepset-ai-haystack-13746`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13746 |
| issue | #12543 (created 2026-09-01) |
| PR created / merged | 2026-11-14 / 2026-11-20 |
| base | `4b4346b6d798338d9b43e70115006494012b1756` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 1 / 42 |
| test files | test/components/evaluators/test_llm_evaluator.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
