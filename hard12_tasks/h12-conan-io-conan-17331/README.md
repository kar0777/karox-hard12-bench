# HARD12 task `h12-conan-io-conan-17331`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/17331 |
| issue | #17324 (created 2024-11-16) |
| PR created / merged | 2024-11-18 / 2026-08-25 |
| base | `7cfe71b6bdcc28d25289c6b445ab36a84677b435` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 2 / 6 |
| test files | test/functional/toolchains/cmake/test_cmake_toolchain_presets.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
