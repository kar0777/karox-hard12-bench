# HARD12 task `h12-pypsa-linopy-1088`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/1088 |
| issue | #1054 (created 2026-10-23) |
| PR created / merged | 2026-10-30 / 2026-10-30 |
| base | `185c001cc1655a54b2ae05003b6e60fd0baf9a2f` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 7 / 152 |
| test files | test/test_constraint.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
