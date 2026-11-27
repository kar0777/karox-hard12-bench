# HARD12 task `h12-pypsa-pypsa-1687`

| item | value |
|---|---|
| source | https://github.com/PyPSA/PyPSA/pull/1687 |
| issue | #1585 (created 2026-03-02) |
| PR created / merged | 2026-05-21 / 2026-06-25 |
| base | `719f9d8b9e5721c2f19f359b81d1e9dfcd947935` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_pypsa-1653:latest` |
| F2P / P2P | 2 / 4 |
| test files | test/test_io.py, test/test_optimization_common.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
