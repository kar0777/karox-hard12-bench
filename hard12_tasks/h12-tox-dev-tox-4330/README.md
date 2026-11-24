# HARD12 task `h12-tox-dev-tox-4330`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/4330 |
| issue | #4227 (created 2026-10-29) |
| PR created / merged | 2026-10-30 / 2026-10-30 |
| base | `e51036dd9a935475159225b14efc877bde798661` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 4 / 137 |
| test files | tests/config/loader/test_str_convert.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
