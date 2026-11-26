# HARD12 task `h12-conan-io-conan-20336`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20336 |
| issue | #20333 (created 2026-09-10) |
| PR created / merged | 2026-09-11 / 2026-09-21 |
| base | `12cf45ebc66d8443ffd6715cf31f68962e108150` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 1 / 9 |
| test files | test/integration/command/install/install_update_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
