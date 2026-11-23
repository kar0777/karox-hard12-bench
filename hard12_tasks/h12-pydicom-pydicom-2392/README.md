# HARD12 task `h12-pydicom-pydicom-2392`

| item | value |
|---|---|
| source | https://github.com/pydicom/pydicom/pull/2392 |
| issue | #2391 (created 2026-10-14) |
| PR created / merged | 2026-10-14 / 2026-11-20 |
| base | `b206fe1469b88529b4170e2b36aae7e6228bc514` |
| image base | `swerebench/sweb.eval.x86_64.pydicom_1776_pydicom-2251:latest` |
| F2P / P2P | 6 / 40 |
| test files | tests/test_util.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
