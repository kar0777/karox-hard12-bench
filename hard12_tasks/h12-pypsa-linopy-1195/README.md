# HARD12 task `h12-pypsa-linopy-1195`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/1195 |
| issue | #1193 (created 2026-11-19) |
| PR created / merged | 2026-11-19 / 2026-11-20 |
| base | `99e123d810d977a79ba9c6cec3d8cf3902b9e202` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 10 / 386 |
| test files | test/test_quadratic_expression.py, test/test_spec_builder.py, test/test_store_conformance.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
