# HARD12 task `h12-conan-io-conan-20088`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20088 |
| issue | #20081 (created 2026-06-12) |
| PR created / merged | 2026-06-17 / 2026-06-24 |
| base | `38bb27a358585c9342746905206a0746d686b843` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 4 / 47 |
| test files | test/functional/toolchains/cmake/cmakeconfigdeps/test_cmakeconfigdeps_new.py, test/integration/toolchains/cmake/cmakeconfigdeps/test_cmakeconfigdeps.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
