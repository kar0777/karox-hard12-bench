# HARD12 task `h12-brianpugh-cyclopts-1008`

| item | value |
|---|---|
| source | https://github.com/BrianPugh/cyclopts/pull/1008 |
| issue | #1002 (created 2026-10-11) |
| PR created / merged | 2026-10-14 / 2026-10-17 |
| base | `7efe101f8e46f8a7ec539bb989fc513a0020f4f1` |
| image base | `swerebench/sweb.eval.x86_64.brianpugh_1776_cyclopts-701:latest` |
| F2P / P2P | 4 / 178 |
| test files | tests/config/test_dict.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
