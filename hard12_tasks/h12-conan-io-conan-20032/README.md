# HARD12 task `h12-conan-io-conan-20032`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20032 |
| issue | #18718 (created 2025-07-30) |
| PR created / merged | 2026-05-28 / 2026-06-26 |
| base | `d8b56378fd088daca39d1627cfcd4dcfcb3867cf` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 5 / 32 |
| test files | test/integration/toolchains/meson/test_mesontoolchain.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
