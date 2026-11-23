# HARD12 task `h12-tox-dev-tox-4434`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/4434 |
| issue | #4432 (created 2026-11-15) |
| PR created / merged | 2026-11-16 / 2026-11-17 |
| base | `7bd2f266415705c30de665c6db63ad82c694912a` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 9 / 74 |
| test files | tests/config/test_main.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
