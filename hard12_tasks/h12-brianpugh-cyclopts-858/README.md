# HARD12 task `h12-brianpugh-cyclopts-858`

| item | value |
|---|---|
| source | https://github.com/BrianPugh/cyclopts/pull/858 |
| issue | #857 (created 2026-07-07) |
| PR created / merged | 2026-07-07 / 2026-07-09 |
| base | `db654ce65d2ae47759b283154c4fa000aa60bcc2` |
| image base | `swerebench/sweb.eval.x86_64.brianpugh_1776_cyclopts-701:latest` |
| F2P / P2P | 12 / 197 |
| test files | tests/test_bind_attrs.py, tests/test_bind_dataclasses.py, tests/test_help.py, tests/test_pydantic.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
