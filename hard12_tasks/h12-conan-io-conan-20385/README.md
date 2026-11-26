# HARD12 task `h12-conan-io-conan-20385`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20385 |
| issue | #17420 (created 2024-12-05) |
| PR created / merged | 2026-10-08 / 2026-10-09 |
| base | `e85a86e84b75a8bc80ba17e19be8df7e5c6df1fa` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 1 / 32 |
| test files | test/integration/cache/backup_sources_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
