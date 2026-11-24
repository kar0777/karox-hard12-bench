# HARD12 task `h12-uxarray-uxarray-1842`

| item | value |
|---|---|
| source | https://github.com/UXARRAY/uxarray/pull/1842 |
| issue | #1599 (created 2026-07-21) |
| PR created / merged | 2026-10-23 / 2026-11-05 |
| base | `f67dba79e015f7585dfd24015aa44ad0853aba1c` |
| image base | `swerebench/sweb.eval.x86_64.uxarray_1776_uxarray-1423:latest` |
| F2P / P2P | 8 / 10 |
| test files | test/grid/integrate/test_basic.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
