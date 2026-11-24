# HARD12 task `h12-aallan-vera-1786`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/1786 |
| issue | #1718 (created 2026-10-16) |
| PR created / merged | 2026-10-22 / 2026-10-22 |
| base | `506d21615f9b53145cc2251849783004b099c6b1` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 14 / 76 |
| test files | tests/test_gc_free_blocks_1718.py, tests/test_matrix_sample.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
