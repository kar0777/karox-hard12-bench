# HARD12 task `h12-uxarray-uxarray-1690`

| item | value |
|---|---|
| source | https://github.com/UXARRAY/uxarray/pull/1690 |
| issue | #1689 (created 2026-08-19) |
| PR created / merged | 2026-08-19 / 2026-08-28 |
| base | `8397815b88c257b0f556c7a139f33ca745b3237e` |
| image base | `swerebench/sweb.eval.x86_64.uxarray_1776_uxarray-1423:latest` |
| F2P / P2P | 1 / 1 |
| test files | test/io/test_structured.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
