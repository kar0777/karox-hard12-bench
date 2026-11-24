# HARD12 task `h12-aallan-vera-1830`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/1830 |
| issue | #1829 (created 2026-11-04) |
| PR created / merged | 2026-11-04 / 2026-11-04 |
| base | `f6d45a787ba66912fe6604089d3e977cefd26031` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 5 / 309 |
| test files | tests/mutation_oracle.py, tests/test_mutate_diff.py, tests/test_mutate_sweep.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
