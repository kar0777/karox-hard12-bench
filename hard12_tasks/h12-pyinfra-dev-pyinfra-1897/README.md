# HARD12 task `h12-pyinfra-dev-pyinfra-1897`

| item | value |
|---|---|
| source | https://github.com/pyinfra-dev/pyinfra/pull/1897 |
| issue | #1860 (created 2026-07-01) |
| PR created / merged | 2026-07-22 / 2026-07-23 |
| base | `138a8ed6a40e0e1b56675c702801f55e25891a99` |
| image base | `swerebench/sweb.eval.x86_64.pyinfra-dev_1776_pyinfra-1679_interface:latest` |
| F2P / P2P | 1 / 0 |
| test files | tests/test_facts_documentation.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
