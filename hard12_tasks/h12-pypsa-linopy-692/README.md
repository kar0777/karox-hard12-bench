# HARD12 task `h12-pypsa-linopy-692`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/692 |
| issue | #688 (created 2026-05-18) |
| PR created / merged | 2026-05-18 / 2026-05-20 |
| base | `c75c55a5496209d99eb782ca12327816aba3fe78` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 37 / 322 |
| test files | test/test_piecewise_constraints.py, test/test_sos_constraints.py, test/test_sos_masked.py, test/test_sos_reformulation.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
