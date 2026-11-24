# HARD12 task `h12-a2aproject-a2a-python-1420`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1420 |
| issue | #1418 (created 2026-11-03) |
| PR created / merged | 2026-11-03 / 2026-11-09 |
| base | `28f8a62f25d46067ae846329a42a60c820fa927e` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 1 / 32 |
| test files | tests/compat/v0_3/test_rest_transport.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
