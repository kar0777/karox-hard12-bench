# HARD12 task `h12-conan-io-conan-20530`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20530 |
| issue | #20527 (created 2026-11-18) |
| PR created / merged | 2026-11-18 / 2026-11-23 |
| base | `57ffc6bec2da672350886beaa16b03cbb6ef675d` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 12 / 21 |
| test files | test/integration/configuration/test_settings_patterns_consumer.py, test/unittests/model/test_recipe_reference.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
