# HARD12 task `h12-stfc-psyclone-3668`

| item | value |
|---|---|
| source | https://github.com/stfc/PSyclone/pull/3668 |
| issue | #3666 (created 2026-11-04) |
| PR created / merged | 2026-11-05 / 2026-11-09 |
| base | `9ccd9c71c4780079d4b99726669c8e8ad81b15de` |
| image base | `swerebench/sweb.eval.x86_64.stfc_1776_psyclone-3093:latest` |
| F2P / P2P | 6 / 64 |
| test files | src/psyclone/tests/psyir/backend/fortran_routine_test.py, src/psyclone/tests/psyir/frontend/fparser2_subroutine_handler_test.py, src/psyclone/tests/psyir/nodes/routine_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
