# HARD12 task `h12-aallan-vera-862`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/862 |
| issue | #755 (created 2026-06-17) |
| PR created / merged | 2026-07-02 / 2026-07-02 |
| base | `99b250bf274bf76c8add04d3ed4ab0c546132c5c` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 6 / 157 |
| test files | tests/test_checker_int_nat.py, tests/test_int_overflow_differential.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
