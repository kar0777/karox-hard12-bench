# HARD12 task `h12-python-wheel-build-fromager-1129`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1129 |
| issue | #1096 (created 2026-04-29) |
| PR created / merged | 2026-05-08 / 2026-05-11 |
| base | `fbe65f7025a7cb22311542833ef48918812a08e0` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 38 / 32 |
| test files | tests/conftest.py, tests/test_cli.py, tests/test_constraints.py, tests/test_context.py, tests/test_cooldown.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
