# HARD12 task `h12-beeware-briefcase-2901`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/2901 |
| issue | #2545 (created 2025-10-31) |
| PR created / merged | 2026-06-22 / 2026-06-25 |
| base | `68b325d1f8da1fadf179da6b3e957723d2133388` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 2 / 7 |
| test files | tests/platforms/linux/system/test_build.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
