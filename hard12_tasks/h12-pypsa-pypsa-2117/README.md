# HARD12 task `h12-pypsa-pypsa-2117`

| item | value |
|---|---|
| source | https://github.com/PyPSA/PyPSA/pull/2117 |
| issue | #2116 (created 2026-11-09) |
| PR created / merged | 2026-11-09 / 2026-11-09 |
| base | `c05731554904616b00dcd59e5efe8823994c8f4d` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_pypsa-1653:latest` |
| F2P / P2P | 3 / 14 |
| test files | test/test_lopf_piecewise_costs.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
