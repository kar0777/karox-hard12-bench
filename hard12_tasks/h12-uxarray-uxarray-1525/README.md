# HARD12 task `h12-uxarray-uxarray-1525`

| item | value |
|---|---|
| source | https://github.com/UXARRAY/uxarray/pull/1525 |
| issue | #1524 (created 2026-06-12) |
| PR created / merged | 2026-06-12 / 2026-06-17 |
| base | `502e6f5311315dc760ce5bb13e7dfb17dac1e824` |
| image base | `swerebench/sweb.eval.x86_64.uxarray_1776_uxarray-1423:latest` |
| F2P / P2P | 3 / 1 |
| test files | test/grid/grid/test_projected.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
