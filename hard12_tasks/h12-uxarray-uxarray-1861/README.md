# HARD12 task `h12-uxarray-uxarray-1861`

| item | value |
|---|---|
| source | https://github.com/UXARRAY/uxarray/pull/1861 |
| issue | #1835 (created 2026-10-21) |
| PR created / merged | 2026-10-28 / 2026-11-20 |
| base | `2f6897a66c44ad82425d0cb93e6fe2f5deac8f4a` |
| image base | `swerebench/sweb.eval.x86_64.uxarray_1776_uxarray-1423:latest` |
| F2P / P2P | 9 / 2 |
| test files | test/io/test_geos.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
