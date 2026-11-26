# HARD12 task `h12-scipp-plopp-603`

| item | value |
|---|---|
| source | https://github.com/scipp/plopp/pull/603 |
| issue | #508 (created 2026-01-21) |
| PR created / merged | 2026-08-07 / 2026-08-10 |
| base | `6abf5c3f8de215e9ca9361c3ec3ecec02c402284` |
| image base | `swerebench/sweb.eval.x86_64.scipp_1776_plopp-513:latest` |
| F2P / P2P | 6 / 7 |
| test files | tests/widgets/clip3d_test.py, tests/widgets/debounce_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
