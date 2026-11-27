# HARD12 task `h12-pyinfra-dev-pyinfra-1666`

| item | value |
|---|---|
| source | https://github.com/pyinfra-dev/pyinfra/pull/1666 |
| issue | #1623 (created 2026-03-21) |
| PR created / merged | 2026-04-14 / 2026-05-12 |
| base | `e85107be0675073e0af3f0df05b5ebee16b5dda0` |
| image base | `swerebench/sweb.eval.x86_64.pyinfra-dev_1776_pyinfra-1679_interface:latest` |
| F2P / P2P | 11 / 64 |
| test files | tests/test_connectors/test_ssh.py, tests/test_connectors/test_util.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
