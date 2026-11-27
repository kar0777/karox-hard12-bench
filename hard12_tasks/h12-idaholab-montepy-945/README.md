# HARD12 task `h12-idaholab-montepy-945`

| item | value |
|---|---|
| source | https://github.com/idaholab/MontePy/pull/945 |
| issue | #737 (created 2025-04-07) |
| PR created / merged | 2026-04-13 / 2026-07-02 |
| base | `19864369ca84033b398bd3957b417129032c0ce5` |
| image base | `swerebench/sweb.eval.x86_64.idaholab_1776_montepy-933_interface:latest` |
| F2P / P2P | 15 / 26 |
| test files | tests/test_geometry.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
