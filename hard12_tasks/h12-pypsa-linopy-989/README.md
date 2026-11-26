# HARD12 task `h12-pypsa-linopy-989`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/989 |
| issue | #986 (created 2026-09-25) |
| PR created / merged | 2026-09-25 / 2026-09-25 |
| base | `26e000d936fb679386535e47191ca0d99aa250f2` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 1 / 1177 |
| test files | test/test_assign_coords.py, test/test_optimization.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
