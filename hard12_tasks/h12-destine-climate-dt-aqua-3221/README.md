# HARD12 task `h12-destine-climate-dt-aqua-3221`

| item | value |
|---|---|
| source | https://github.com/DestinE-Climate-DT/AQUA/pull/3221 |
| issue | #3190 (created 2026-10-08) |
| PR created / merged | 2026-10-13 / 2026-10-20 |
| base | `479a592fa7c166d4bb74ba9b4de8ba10a3070c86` |
| image base | `swerebench/sweb.eval.x86_64.destine-climate-dt_1776_aqua-2768:latest` |
| F2P / P2P | 6 / 14 |
| test files | tests/test_safelock.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
