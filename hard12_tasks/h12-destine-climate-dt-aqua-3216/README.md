# HARD12 task `h12-destine-climate-dt-aqua-3216`

| item | value |
|---|---|
| source | https://github.com/DestinE-Climate-DT/AQUA/pull/3216 |
| issue | #3212 (created 2026-10-12) |
| PR created / merged | 2026-10-13 / 2026-10-13 |
| base | `5c57675aa88f3217f834842af4cfffb0bfb6f400` |
| image base | `swerebench/sweb.eval.x86_64.destine-climate-dt_1776_aqua-2768:latest` |
| F2P / P2P | 1 / 12 |
| test files | tests/console/test_console_base.py, tests/console/test_console_shared.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
