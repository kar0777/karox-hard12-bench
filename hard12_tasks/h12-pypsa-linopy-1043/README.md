# HARD12 task `h12-pypsa-linopy-1043`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/1043 |
| issue | #1018 (created 2026-10-07) |
| PR created / merged | 2026-10-22 / 2026-10-22 |
| base | `f6da2877a2d7a00f064fd94daa1065839b553615` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 16 / 960 |
| test files | test/test_csr.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
