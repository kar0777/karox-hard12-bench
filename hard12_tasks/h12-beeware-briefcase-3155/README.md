# HARD12 task `h12-beeware-briefcase-3155`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/3155 |
| issue | #3150 (created 2026-11-14) |
| PR created / merged | 2026-11-16 / 2026-11-19 |
| base | `57d29bdd81be67339f210c807e32e9af4a2826ae` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 1 / 51 |
| test files | tests/integrations/android_sdk/AndroidSDK/test_select_target_device.py, tests/integrations/xcode/test_get_simulators.py, tests/platforms/iOS/xcode/mixin/test_select_target_device.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
