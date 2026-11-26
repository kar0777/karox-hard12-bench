# HARD12 task `h12-pypsa-linopy-907`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/907 |
| issue | #906 (created 2026-08-27) |
| PR created / merged | 2026-08-27 / 2026-09-02 |
| base | `9117fea7719763b8b0b356b42d4f6c837e430222` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 2 / 638 |
| test files | test/test_linear_expression.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
