# HARD12 task `h12-conan-io-conan-20539`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20539 |
| issue | #20535 (created 2026-11-19) |
| PR created / merged | 2026-11-19 / 2026-11-20 |
| base | `8ea72a2229e8f57a3bdceecf02b4a2076ed51fd9` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 3 / 5 |
| test files | test/integration/package_id/transitive_options_affect_id_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
