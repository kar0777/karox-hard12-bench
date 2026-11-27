# HARD12 task `h12-pypsa-linopy-798`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/798 |
| issue | #796 (created 2026-06-29) |
| PR created / merged | 2026-06-29 / 2026-06-30 |
| base | `2d47d4ab312fd7473af4311181b47ccdff654e7b` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 21 / 0 |
| test files | test/test_piecewise_active_fill.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
