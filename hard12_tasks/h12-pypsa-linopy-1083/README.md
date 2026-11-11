# HARD12 task `h12-pypsa-linopy-1083`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/1083 |
| issue | #1077 (created 2026-10-28) |
| PR created / merged | 2026-10-28 / 2026-10-30 |
| base | `6496bab61aef6e77070102e8d81ef77d6c5da673` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 2 / 18 |
| test files | test/test_scaling.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
