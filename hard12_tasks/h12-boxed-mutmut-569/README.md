# HARD12 task `h12-boxed-mutmut-569`

| item | value |
|---|---|
| source | https://github.com/boxed/mutmut/pull/569 |
| issue | #564 (created 2026-09-04) |
| PR created / merged | 2026-09-08 / 2026-09-12 |
| base | `7f8ba005185ac98216cbeedfcacffeb4229366fa` |
| image base | `swerebench/sweb.eval.x86_64.boxed_1776_mutmut-403:latest` |
| F2P / P2P | 2 / 1 |
| test files | tests/runners/__init__.py, tests/runners/test_harness.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
