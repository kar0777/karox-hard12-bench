# HARD12 task `h12-pyinfra-dev-pyinfra-1751`

| item | value |
|---|---|
| source | https://github.com/pyinfra-dev/pyinfra/pull/1751 |
| issue | #1729 (created 2026-05-06) |
| PR created / merged | 2026-05-14 / 2026-05-19 |
| base | `d3bc74b5d7796034398dc6195fcb5dfa534065a3` |
| image base | `swerebench/sweb.eval.x86_64.pyinfra-dev_1776_pyinfra-1679_interface:latest` |
| F2P / P2P | 1 / 8 |
| test files | tests/test_api/test_api_host.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
