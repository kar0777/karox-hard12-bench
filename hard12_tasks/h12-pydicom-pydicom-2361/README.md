# HARD12 task `h12-pydicom-pydicom-2361`

| item | value |
|---|---|
| source | https://github.com/pydicom/pydicom/pull/2361 |
| issue | #2340 (created 2026-06-25) |
| PR created / merged | 2026-09-01 / 2026-09-17 |
| base | `d80e8b1791f7a3dfd753f36400abc9f9941423f2` |
| image base | `swerebench/sweb.eval.x86_64.pydicom_1776_pydicom-2251:latest` |
| F2P / P2P | 1 / 16 |
| test files | tests/pixels/test_encoder_base.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
