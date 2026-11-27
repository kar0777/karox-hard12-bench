# HARD12 task `h12-beeware-briefcase-2840`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/2840 |
| issue | #2127 (created 2025-01-21) |
| PR created / merged | 2026-05-18 / 2026-06-03 |
| base | `6368df00105a2c59af752c515cf95ab242fba6ca` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 7 / 152 |
| test files | tests/commands/convert/test_input_app_name.py, tests/commands/new/test_validate_app_name.py, tests/config/test_AppConfig.py, tests/config/test_is_valid_app_name.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
