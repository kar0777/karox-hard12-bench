# HARD12 task `h12-conan-io-conan-20347`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20347 |
| issue | #20345 (created 2026-09-22) |
| PR created / merged | 2026-09-22 / 2026-09-23 |
| base | `b7bfd2dc2bf44643432b199800d1ef5582d171e6` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 3 / 50 |
| test files | test/functional/toolchains/cmake/cmakeconfigdeps/test_cmakeconfigdeps_objects.py, test/integration/toolchains/cmake/cmakeconfigdeps/test_cmakeconfigdeps.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
