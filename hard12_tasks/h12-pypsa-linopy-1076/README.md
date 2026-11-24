# HARD12 task `h12-pypsa-linopy-1076`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/1076 |
| issue | #1055 (created 2026-10-23) |
| PR created / merged | 2026-10-27 / 2026-10-30 |
| base | `9ad435d3dc9622682fbac122ba59ade8c28b5b14` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 4 / 381 |
| test files | test/test_linear_expression.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
