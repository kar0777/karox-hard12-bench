# HARD12 task `h12-scipp-plopp-595`

| item | value |
|---|---|
| source | https://github.com/scipp/plopp/pull/595 |
| issue | #589 (created 2026-07-26) |
| PR created / merged | 2026-07-30 / 2026-07-31 |
| base | `1fc5473c309bd0aad64027705d92cb0622e5c9d0` |
| image base | `swerebench/sweb.eval.x86_64.scipp_1776_plopp-513:latest` |
| F2P / P2P | 15 / 0 |
| test files | tests/backends/matplotlib/mpl_utils_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
