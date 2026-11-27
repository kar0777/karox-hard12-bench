# HARD12 task `h12-brianpugh-cyclopts-825`

| item | value |
|---|---|
| source | https://github.com/BrianPugh/cyclopts/pull/825 |
| issue | #821 (created 2026-05-24) |
| PR created / merged | 2026-05-25 / 2026-05-25 |
| base | `e297647b12b71155d01f87e8e1d5e008c90962b6` |
| image base | `swerebench/sweb.eval.x86_64.brianpugh_1776_cyclopts-701:latest` |
| F2P / P2P | 3 / 24 |
| test files | tests/completion/conftest.py, tests/completion/test_install.py, tests/completion/test_zsh.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
