# HARD12 task `h12-pypsa-pypsa-2189`

| item | value |
|---|---|
| source | https://github.com/PyPSA/PyPSA/pull/2189 |
| issue | #2187 (created 2026-11-22) |
| PR created / merged | 2026-11-22 / 2026-11-23 |
| base | `7dee89a06b945d3c65acbce0b587110672a695b3` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_pypsa-1653:latest` |
| F2P / P2P | 2 / 93 |
| test files | test/test_lopf_mga.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
