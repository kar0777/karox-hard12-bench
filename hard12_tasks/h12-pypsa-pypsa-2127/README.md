# HARD12 task `h12-pypsa-pypsa-2127`

| item | value |
|---|---|
| source | https://github.com/PyPSA/PyPSA/pull/2127 |
| issue | #1602 (created 2026-03-04) |
| PR created / merged | 2026-11-11 / 2026-11-13 |
| base | `3625c8168b0b45a7936ddcb3a4da99dd608125ca` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_pypsa-1653:latest` |
| F2P / P2P | 2 / 63 |
| test files | test/test_consistency_check.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
