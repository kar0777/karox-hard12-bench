# HARD12 task `h12-pypsa-pypsa-1961`

| item | value |
|---|---|
| source | https://github.com/PyPSA/PyPSA/pull/1961 |
| issue | #1954 (created 2026-09-29) |
| PR created / merged | 2026-10-01 / 2026-10-01 |
| base | `2c1fa2b22a7951ac8342d3e90c1f962c34200724` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_pypsa-1653:latest` |
| F2P / P2P | 2 / 3 |
| test files | test/test_lopf_global_constraints.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
