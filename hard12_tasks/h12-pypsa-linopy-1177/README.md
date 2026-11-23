# HARD12 task `h12-pypsa-linopy-1177`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/1177 |
| issue | #1176 (created 2026-11-18) |
| PR created / merged | 2026-11-18 / 2026-11-19 |
| base | `a85e7b111bbf2b4336759d6caea769b25b9d04bc` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 4 / 576 |
| test files | test/test_optimization.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
