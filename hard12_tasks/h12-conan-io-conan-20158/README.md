# HARD12 task `h12-conan-io-conan-20158`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20158 |
| issue | #20153 (created 2026-07-07) |
| PR created / merged | 2026-07-08 / 2026-08-14 |
| base | `31d43558c1b964e0c9fb31c12bd36c4136b7ca66` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 1 / 69 |
| test files | test/integration/toolchains/cmake/test_cmaketoolchain.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
