# HARD12 task `h12-conan-io-conan-20102`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20102 |
| issue | #20031 (created 2026-05-28) |
| PR created / merged | 2026-06-22 / 2026-07-20 |
| base | `ea318dfeaea2501aee4bafbaa507d2ebab300a8f` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 7 / 43 |
| test files | test/integration/package_id/package_id_modes_test.py, test/integration/package_id/package_id_requires_modes_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
