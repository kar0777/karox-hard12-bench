# HARD12 task `h12-pymc-devs-pymc-8302`

| item | value |
|---|---|
| source | https://github.com/pymc-devs/pymc/pull/8302 |
| issue | #8301 (created 2026-05-16) |
| PR created / merged | 2026-05-17 / 2026-05-18 |
| base | `169e90128cf0c58e76350b1d21a1cfcd65d2ef79` |
| image base | `swerebench/sweb.eval.x86_64.pymc-devs_1776_pymc-7858:latest` |
| F2P / P2P | 1 / 27 |
| test files | tests/logprob/test_basic.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
