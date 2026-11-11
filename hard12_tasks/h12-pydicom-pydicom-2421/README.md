# HARD12 task `h12-pydicom-pydicom-2421`

| item | value |
|---|---|
| source | https://github.com/pydicom/pydicom/pull/2421 |
| issue | #2420 (created 2026-11-03) |
| PR created / merged | 2026-11-03 / 2026-11-05 |
| base | `db6c2f5775c0b8fa8b87c0303ee6fa7d7bffc5c6` |
| image base | `swerebench/sweb.eval.x86_64.pydicom_1776_pydicom-2251:latest` |
| F2P / P2P | 5 / 375 |
| test files | tests/test_filereader.py, tests/test_filewriter.py, tests/test_json.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
