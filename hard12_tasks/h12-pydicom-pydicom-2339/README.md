# HARD12 task `h12-pydicom-pydicom-2339`

| item | value |
|---|---|
| source | https://github.com/pydicom/pydicom/pull/2339 |
| issue | #2338 (created 2026-06-16) |
| PR created / merged | 2026-06-18 / 2026-11-17 |
| base | `4b619464cafcdd3b6a5daa2ef4c8a08251380f01` |
| image base | `swerebench/sweb.eval.x86_64.pydicom_1776_pydicom-2251:latest` |
| F2P / P2P | 3 / 48 |
| test files | tests/test_charset.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
