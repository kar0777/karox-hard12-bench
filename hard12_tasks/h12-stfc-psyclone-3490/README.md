# HARD12 task `h12-stfc-psyclone-3490`

| item | value |
|---|---|
| source | https://github.com/stfc/PSyclone/pull/3490 |
| issue | #3488 (created 2026-07-08) |
| PR created / merged | 2026-07-08 / 2026-07-17 |
| base | `665206a28e004560228c525c157aca51996182f5` |
| image base | `swerebench/sweb.eval.x86_64.stfc_1776_psyclone-3093:latest` |
| F2P / P2P | 1 / 35 |
| test files | src/psyclone/tests/psyir/frontend/fparser2_where_handler_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
