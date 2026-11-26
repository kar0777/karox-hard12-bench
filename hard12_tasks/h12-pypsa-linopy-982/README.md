# HARD12 task `h12-pypsa-linopy-982`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/982 |
| issue | #981 (created 2026-09-24) |
| PR created / merged | 2026-09-25 / 2026-09-25 |
| base | `bee7d1f053db741e2540697599c479c2cb849b79` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 10 / 597 |
| test files | test/test_csr.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
