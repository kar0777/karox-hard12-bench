# HARD12 task `h12-brianpugh-cyclopts-843`

| item | value |
|---|---|
| source | https://github.com/BrianPugh/cyclopts/pull/843 |
| issue | #842 (created 2026-06-26) |
| PR created / merged | 2026-06-26 / 2026-06-29 |
| base | `e475acd2a8b9128919b429178f8173b62715c749` |
| image base | `swerebench/sweb.eval.x86_64.brianpugh_1776_cyclopts-701:latest` |
| F2P / P2P | 1 / 97 |
| test files | tests/test_bind_basic.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
