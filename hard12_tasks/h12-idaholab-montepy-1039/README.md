# HARD12 task `h12-idaholab-montepy-1039`

| item | value |
|---|---|
| source | https://github.com/idaholab/MontePy/pull/1039 |
| issue | #1037 (created 2026-11-01) |
| PR created / merged | 2026-11-02 / 2026-11-02 |
| base | `4af4cb0b6d42177ef92bc8924dfb841f2d7c4c9f` |
| image base | `swerebench/sweb.eval.x86_64.idaholab_1776_montepy-933_interface:latest` |
| F2P / P2P | 6 / 206 |
| test files | tests/test_syntax_parsing.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
