# HARD12 task `h12-pyinfra-dev-pyinfra-1853`

| item | value |
|---|---|
| source | https://github.com/pyinfra-dev/pyinfra/pull/1853 |
| issue | #1798 (created 2026-06-10) |
| PR created / merged | 2026-06-24 / 2026-07-14 |
| base | `0566cf48b7d030f0b64ea87312bceb05b6c1f310` |
| image base | `swerebench/sweb.eval.x86_64.pyinfra-dev_1776_pyinfra-1679_interface:latest` |
| F2P / P2P | 2 / 41 |
| test files | tests/test_connectors/test_util.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
