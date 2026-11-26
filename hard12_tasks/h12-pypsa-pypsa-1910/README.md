# HARD12 task `h12-pypsa-pypsa-1910`

| item | value |
|---|---|
| source | https://github.com/PyPSA/PyPSA/pull/1910 |
| issue | #1481 (created 2025-12-10) |
| PR created / merged | 2026-09-07 / 2026-09-16 |
| base | `1168ef06df514cae66bbdbab9d35b874e8adb871` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_pypsa-1653:latest` |
| F2P / P2P | 1 / 15 |
| test files | test/test_lopf_basic_constraints.py, test/test_lopf_iteratively.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
