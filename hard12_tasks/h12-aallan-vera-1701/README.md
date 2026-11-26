# HARD12 task `h12-aallan-vera-1701`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/1701 |
| issue | #1671 (created 2026-10-13) |
| PR created / merged | 2026-10-14 / 2026-10-14 |
| base | `a5b5de8f79028db5bd180b22cd01222b970e5d12` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 33 / 204 |
| test files | tests/test_match_unknown_scrutinee_1671.py, tests/test_matrix_sample.py, tests/test_result_reference_type_1517.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
