# HARD12 task `h12-beeware-briefcase-2959`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/2959 |
| issue | #1890 (created 2024-06-27) |
| PR created / merged | 2026-07-23 / 2026-07-24 |
| base | `5370a8b3b7b632535ac2f2dfdaded51f9a939dbe` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 2 / 22 |
| test files | tests/platforms/windows/app/test_package.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
