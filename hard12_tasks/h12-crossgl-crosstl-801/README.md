# HARD12 task `h12-crossgl-crosstl-801`

| item | value |
|---|---|
| source | https://github.com/CrossGL/crosstl/pull/801 |
| issue | #795 (created 2026-06-10) |
| PR created / merged | 2026-06-10 / 2026-06-10 |
| base | `329dcbd67420f9cea48122292ee1c6653a59c2e1` |
| image base | `swerebench/sweb.eval.x86_64.crossgl_1776_crosstl-257:latest` |
| F2P / P2P | 6 / 880 |
| test files | tests/test_backend/test_HIP/test_codegen.py, tests/test_translator/test_project_translation.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
