# HARD12 task `h12-conan-io-conan-20040`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20040 |
| issue | #20035 (created 2026-05-28) |
| PR created / merged | 2026-05-29 / 2026-06-09 |
| base | `23351d838cb8352a6e60369e7002ca1ebe640af6` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 5 / 87 |
| test files | test/integration/graph/test_replace_requires.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
