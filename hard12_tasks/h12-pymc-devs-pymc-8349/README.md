# HARD12 task `h12-pymc-devs-pymc-8349`

| item | value |
|---|---|
| source | https://github.com/pymc-devs/pymc/pull/8349 |
| issue | #8307 (created 2026-05-20) |
| PR created / merged | 2026-07-06 / 2026-07-06 |
| base | `c032457ef2279b4fff7c0fce2cc73f7b212d2878` |
| image base | `swerebench/sweb.eval.x86_64.pymc-devs_1776_pymc-7858:latest` |
| F2P / P2P | 1 / 52 |
| test files | tests/distributions/test_custom.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
