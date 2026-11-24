# HARD12 task `h12-beeware-briefcase-3136`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/3136 |
| issue | #1024 (created 2022-12-31) |
| PR created / merged | 2026-11-07 / 2026-11-08 |
| base | `d94b1eb06d55d1cf01559f8818b1df0625a3ea3d` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 13 / 24 |
| test files | tests/integrations/android_sdk/AndroidSDK/test__create_emulator.py, tests/integrations/android_sdk/AndroidSDK/test_avd_config.py, tests/integrations/android_sdk/AndroidSDK/test_update_emulator_config.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
