# HARD12 task `h12-stfc-psyclone-3468`

| item | value |
|---|---|
| source | https://github.com/stfc/PSyclone/pull/3468 |
| issue | #3461 (created 2026-06-23) |
| PR created / merged | 2026-06-25 / 2026-09-01 |
| base | `b863aea4d558244a2a12a226b530954bd02f97d9` |
| image base | `swerebench/sweb.eval.x86_64.stfc_1776_psyclone-3093:latest` |
| F2P / P2P | 9 / 79 |
| test files | src/psyclone/tests/generator_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
