# HARD12 task `h12-copier-org-copier-2849`

| item | value |
|---|---|
| source | https://github.com/copier-org/copier/pull/2849 |
| issue | #2763 (created 2026-07-16) |
| PR created / merged | 2026-09-16 / 2026-10-06 |
| base | `217e4f87828694df89e1513a1febdc33792f6e89` |
| image base | `swerebench/sweb.eval.x86_64.copier-org_1776_copier-2646:latest` |
| F2P / P2P | 4 / 352 |
| test files | tests/test_complex_questions.py, tests/test_prompt.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
