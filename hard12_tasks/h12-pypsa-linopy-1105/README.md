# HARD12 task `h12-pypsa-linopy-1105`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/1105 |
| issue | #368 (created 2024-10-30) |
| PR created / merged | 2026-11-02 / 2026-11-02 |
| base | `4b949a5d24f8da63ad40850c5aa7a34ba19c4be5` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 1 / 68 |
| test files | test/test_solvers.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
