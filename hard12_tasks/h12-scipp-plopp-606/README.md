# HARD12 task `h12-scipp-plopp-606`

| item | value |
|---|---|
| source | https://github.com/scipp/plopp/pull/606 |
| issue | #384 (created 2024-10-28) |
| PR created / merged | 2026-08-14 / 2026-09-14 |
| base | `3b86d5a9469b251f932e93979bf5d06cb32c0640` |
| image base | `swerebench/sweb.eval.x86_64.scipp_1776_plopp-513:latest` |
| F2P / P2P | 9 / 24 |
| test files | tests/backends/pythreejs/pythreejs_scatter3d_test.py, tests/widgets/clip3d_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
