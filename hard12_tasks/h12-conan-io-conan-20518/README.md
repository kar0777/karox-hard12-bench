# HARD12 task `h12-conan-io-conan-20518`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20518 |
| issue | #20513 (created 2026-11-17) |
| PR created / merged | 2026-11-17 / 2026-11-17 |
| base | `14a906d4b360d0fadef572d6438a17475ffad43d` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 15 / 89 |
| test files | test/integration/graph/conflict_diamond_test.py, test/unittests/model/version/test_version_range_intersection.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
