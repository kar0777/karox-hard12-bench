# HARD12 task `h12-pypsa-pypsa-2099`

| item | value |
|---|---|
| source | https://github.com/PyPSA/PyPSA/pull/2099 |
| issue | #2093 (created 2026-11-04) |
| PR created / merged | 2026-11-04 / 2026-11-04 |
| base | `45b566348c9a088dc5dd15ca02ad42ea32de6156` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_pypsa-1653:latest` |
| F2P / P2P | 4 / 62 |
| test files | test/test_lopf_multiinvest.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
