# HARD12 task `h12-tox-dev-tox-4172`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/4172 |
| issue | #4169 (created 2026-10-17) |
| PR created / merged | 2026-10-17 / 2026-10-18 |
| base | `ba393c1b2a3a4c264ece98aa574a85dcac94148e` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 6 / 153 |
| test files | tests/config/source/test_toml_pyproject.py, tests/config/test_types.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
