# HARD12 task `h12-pypsa-linopy-1113`

| item | value |
|---|---|
| source | https://github.com/PyPSA/linopy/pull/1113 |
| issue | #1111 (created 2026-11-02) |
| PR created / merged | 2026-11-02 / 2026-11-02 |
| base | `74a1f62e5dfd982fae06130d0d2fd7b3bfcbc74d` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_linopy-494:latest` |
| F2P / P2P | 4 / 100 |
| test files | test/test_restrict_matrix.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
