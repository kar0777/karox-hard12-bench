# HARD12 task `h12-conan-io-conan-20449`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20449 |
| issue | #20447 (created 2026-10-27) |
| PR created / merged | 2026-10-28 / 2026-10-30 |
| base | `4b189808f92a2a3127c6f5a8f52762b97aa4dd03` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 15 / 18 |
| test files | test/integration/graph/test_requires_traits_order.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
