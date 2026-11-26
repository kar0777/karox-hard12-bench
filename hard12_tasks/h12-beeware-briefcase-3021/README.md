# HARD12 task `h12-beeware-briefcase-3021`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/3021 |
| issue | #3016 (created 2026-08-23) |
| PR created / merged | 2026-08-24 / 2026-08-24 |
| base | `65a21346d991166d0b3f922f13fd381594153824` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 5 / 43 |
| test files | tests/commands/convert/test_build_app_context.py, tests/commands/convert/test_input_license.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
