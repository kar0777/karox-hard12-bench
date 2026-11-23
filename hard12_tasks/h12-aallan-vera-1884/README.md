# HARD12 task `h12-aallan-vera-1884`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/1884 |
| issue | #1635 (created 2026-10-09) |
| PR created / merged | 2026-11-18 / 2026-11-18 |
| base | `1e520fc666c1040400fe30f9a45108b3255ac83c` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 37 / 514 |
| test files | tests/test_matrix_sample.py, tests/test_negation_overflow_1875.py, tests/test_reconciliation.py, tests/test_verifier_adt_decreases.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
