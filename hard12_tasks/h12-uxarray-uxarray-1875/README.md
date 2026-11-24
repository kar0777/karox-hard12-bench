# HARD12 task `h12-uxarray-uxarray-1875`

| item | value |
|---|---|
| source | https://github.com/UXARRAY/uxarray/pull/1875 |
| issue | #1758 (created 2026-09-14) |
| PR created / merged | 2026-11-04 / 2026-11-23 |
| base | `8423b24635ec6b1939548b9e411dfc10d06d3d38` |
| image base | `swerebench/sweb.eval.x86_64.uxarray_1776_uxarray-1423:latest` |
| F2P / P2P | 2 / 13 |
| test files | test/core/test_indexing.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
