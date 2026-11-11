# HARD12 task `h12-aallan-vera-1760`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/1760 |
| issue | #1756 (created 2026-10-21) |
| PR created / merged | 2026-10-21 / 2026-10-21 |
| base | `367d84d7988d58dd07e1dc46392a6d64d482e49a` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 7 / 123 |
| test files | tests/test_literal_branch_join_1756.py, tests/test_matrix_sample.py, tests/test_program_generator.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
