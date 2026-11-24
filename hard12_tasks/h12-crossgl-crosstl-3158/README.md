# HARD12 task `h12-crossgl-crosstl-3158`

| item | value |
|---|---|
| source | https://github.com/CrossGL/crosstl/pull/3158 |
| issue | #3087 (created 2026-10-25) |
| PR created / merged | 2026-10-26 / 2026-10-26 |
| base | `6eeda6269b22141ed8ad296c840a8bf0438ee507` |
| image base | `swerebench/sweb.eval.x86_64.crossgl_1776_crosstl-257:latest` |
| F2P / P2P | 9 / 69 |
| test files | tests/test_backend/test_OpenCL/test_codegen.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
