# HARD12 task `h12-uxarray-uxarray-1646`

| item | value |
|---|---|
| source | https://github.com/UXARRAY/uxarray/pull/1646 |
| issue | #1645 (created 2026-08-04) |
| PR created / merged | 2026-08-04 / 2026-08-06 |
| base | `fa82d7b9a2b3396774a794d52630f0d632f207bb` |
| image base | `swerebench/sweb.eval.x86_64.uxarray_1776_uxarray-1423:latest` |
| F2P / P2P | 2 / 8 |
| test files | test/grid/grid/test_areas.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
