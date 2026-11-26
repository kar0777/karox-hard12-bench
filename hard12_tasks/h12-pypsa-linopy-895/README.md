# HARD12 task `h12-pypsa-linopy-895`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/895 |
| issue | #883 (created 2026-08-07) |
| PR created / merged | 2026-08-17 / 2026-08-18 |
| base | `5d22e35524ca26ef19e4052054ee45579cd4cc97` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 3 / 25 |
| test files | test/test_model.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
