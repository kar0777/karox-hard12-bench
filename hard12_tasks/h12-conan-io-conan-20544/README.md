# HARD12 task `h12-conan-io-conan-20544`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20544 |
| issue | #20542 (created 2026-11-19) |
| PR created / merged | 2026-11-20 / 2026-11-20 |
| base | `57ffc6bec2da672350886beaa16b03cbb6ef675d` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 1 / 25 |
| test files | test/integration/command/export_pkg_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
