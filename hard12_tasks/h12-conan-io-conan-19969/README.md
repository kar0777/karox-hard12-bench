# HARD12 task `h12-conan-io-conan-19969`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/19969 |
| issue | #19956 (created 2026-05-08) |
| PR created / merged | 2026-05-11 / 2026-05-13 |
| base | `541aa0ced021090979f363288992e61743fcdc70` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 2 / 30 |
| test files | conan/test/assets/genconanfile.py, test/integration/cache/backup_sources_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
