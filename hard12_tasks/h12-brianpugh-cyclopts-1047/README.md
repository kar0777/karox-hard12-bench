# HARD12 task `h12-brianpugh-cyclopts-1047`

| item | value |
|---|---|
| source | https://github.com/BrianPugh/cyclopts/pull/1047 |
| issue | #1044 (created 2026-11-05) |
| PR created / merged | 2026-11-05 / 2026-11-05 |
| base | `e512a49fa3fc46f8abe6ad05d9b4a782db80677a` |
| image base | `swerebench/sweb.eval.x86_64.brianpugh_1776_cyclopts-701:latest` |
| F2P / P2P | 5 / 74 |
| test files | tests/test_bind_converter_validator.py, tests/test_exceptions_rich.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
