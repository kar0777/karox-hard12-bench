# HARD12 task `h12-conan-io-conan-20472`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20472 |
| issue | #19433 (created 2026-01-05) |
| PR created / merged | 2026-11-04 / 2026-11-12 |
| base | `5e81799e9e4538f84df35e90613d6a2c5e668bb1` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 1 / 3 |
| test files | test/integration/configuration/proxies_conf_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
