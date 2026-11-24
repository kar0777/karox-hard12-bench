# HARD12 task `h12-beeware-briefcase-3130`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/3130 |
| issue | #3129 (created 2026-11-04) |
| PR created / merged | 2026-11-04 / 2026-11-06 |
| base | `fee777ed204fe867a8486d8947137dacdb7f05f4` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 7 / 190 |
| test files | tests/commands/dev/conftest.py, tests/commands/dev/test_call.py, tests/commands/run/conftest.py, tests/commands/run/test_call.py, tests/config/test_GlobalConfig.py, tests/config/test_parse_config.py, tests/platforms/android/gradle/test_run.py, tests/platforms/linux/appimage/test_run.py, tests/platforms/linux/system/test_dev.py, tests/platforms/linux/system/test_run.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
