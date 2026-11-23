# HARD12 task `h12-deepset-ai-haystack-13832`

| item | value |
|---|---|
| source | https://github.com/deepset-ai/haystack/pull/13832 |
| issue | #13680 (created 2026-11-11) |
| PR created / merged | 2026-11-20 / 2026-11-20 |
| base | `eabc8ed8b2f410febb41e77c9ff243aa848cdb4c` |
| image base | `swerebench/sweb.eval.x86_64.deepset-ai_1776_haystack-10547:latest` |
| F2P / P2P | 2 / 138 |
| test files | test/components/agents/test_agent.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
