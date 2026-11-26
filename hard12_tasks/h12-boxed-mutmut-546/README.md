# HARD12 task `h12-boxed-mutmut-546`

| item | value |
|---|---|
| source | https://github.com/boxed/mutmut/pull/546 |
| issue | #196 (created 2021-01-08) |
| PR created / merged | 2026-08-02 / 2026-08-02 |
| base | `4f1208093517575a9402b99cfdcc7dea54c40e67` |
| image base | `swerebench/sweb.eval.x86_64.boxed_1776_mutmut-403:latest` |
| F2P / P2P | 1 / 189 |
| test files | tests/mutation/test_mutation.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
