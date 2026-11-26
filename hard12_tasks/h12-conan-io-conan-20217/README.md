# HARD12 task `h12-conan-io-conan-20217`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20217 |
| issue | #18981 (created 2025-09-23) |
| PR created / merged | 2026-07-27 / 2026-07-28 |
| base | `db1ebb70cd3d3636448ffffd64d64984ce66a117` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 3 / 21 |
| test files | test/integration/command/export/export_sources_test.py, test/unittests/tools/files/test_tool_copy.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
