# HARD12 task `h12-pydicom-pydicom-2396`

| item | value |
|---|---|
| source | https://github.com/pydicom/pydicom/pull/2396 |
| issue | #2395 (created 2026-10-16) |
| PR created / merged | 2026-10-16 / 2026-10-29 |
| base | `6f92f30ce79132672d59a3731c9e6072f7fd2ee6` |
| image base | `swerebench/sweb.eval.x86_64.pydicom_1776_pydicom-2251:latest` |
| F2P / P2P | 2 / 192 |
| test files | tests/test_dataset.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
