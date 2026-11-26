# HARD12 task `h12-uxarray-uxarray-1531`

| item | value |
|---|---|
| source | https://github.com/UXARRAY/uxarray/pull/1531 |
| issue | #463 (created 2023-09-19) |
| PR created / merged | 2026-06-23 / 2026-07-13 |
| base | `df6ef32d3e5a144d0537ac3f197ba2db8ea1b8ca` |
| image base | `swerebench/sweb.eval.x86_64.uxarray_1776_uxarray-1423:latest` |
| F2P / P2P | 3 / 8 |
| test files | test/core/test_dataset.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
