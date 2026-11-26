# HARD12 task `h12-a2aproject-a2a-python-1277`

| item | value |
|---|---|
| source | https://github.com/a2aproject/a2a-python/pull/1277 |
| issue | #1276 (created 2026-09-24) |
| PR created / merged | 2026-09-24 / 2026-09-30 |
| base | `041c17bbe8d5ced7a8f6c48761152ce01ffbfc14` |
| image base | `swerebench/sweb.eval.x86_64.a2aproject_1776_a2a-python-682_interface:latest` |
| F2P / P2P | 2 / 22 |
| test files | tests/compat/v0_3/test_proto_utils.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
