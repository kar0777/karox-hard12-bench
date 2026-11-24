# HARD12 task `h12-conan-io-conan-20510`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/20510 |
| issue | #20500 (created 2026-11-14) |
| PR created / merged | 2026-11-16 / 2026-11-16 |
| base | `49d320e7183187de0e1f4e0c924dd8b8e067eccc` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 4 / 8 |
| test files | test/unittests/tools/sbom/test_spdx_expression.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
