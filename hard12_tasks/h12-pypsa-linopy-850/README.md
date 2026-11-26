# HARD12 task `h12-pypsa-linopy-850`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/850 |
| issue | #849 (created 2026-07-16) |
| PR created / merged | 2026-07-20 / 2026-07-20 |
| base | `40c2022b18932b68122b65ab685c1ff536b18149` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 1 / 288 |
| test files | test/test_legacy_violations.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
