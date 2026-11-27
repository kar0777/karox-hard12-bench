# HARD12 task `h12-pypsa-linopy-777`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/777 |
| issue | #776 (created 2026-06-11) |
| PR created / merged | 2026-06-13 / 2026-06-19 |
| base | `31b677896405205acc9c49e20a3c80d0b0a4d561` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 2 / 35 |
| test files | test/test_io.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
