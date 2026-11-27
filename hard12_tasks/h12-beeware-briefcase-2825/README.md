# HARD12 task `h12-beeware-briefcase-2825`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/2825 |
| issue | #2824 (created 2026-05-13) |
| PR created / merged | 2026-05-14 / 2026-05-14 |
| base | `2cedd51bd0d7134074d2d8db5d062e15d16c9bbf` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 4 / 101 |
| test files | tests/config/test_AppConfig.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
