# HARD12 task `h12-pydicom-pydicom-2423`

| item | value |
|---|---|
| source | https://github.com/pydicom/pydicom/pull/2423 |
| issue | #2422 (created 2026-11-04) |
| PR created / merged | 2026-11-04 / 2026-11-17 |
| base | `ff1dd5a6dc3bfa6f78a13ede7349cb8d4c575829` |
| image base | `swerebench/sweb.eval.x86_64.pydicom_1776_pydicom-2251:latest` |
| F2P / P2P | 3 / 320 |
| test files | tests/test_valuerep.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
