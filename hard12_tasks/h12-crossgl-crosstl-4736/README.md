# HARD12 task `h12-crossgl-crosstl-4736`

| item | value |
|---|---|
| source | https://github.com/CrossGL/crosstl/pull/4736 |
| issue | #4636 (created 2026-11-19) |
| PR created / merged | 2026-11-20 / 2026-11-21 |
| base | `869d1a15f7463dd210bf00c87c5990264cb2946e` |
| image base | `swerebench/sweb.eval.x86_64.crossgl_1776_crosstl-257:latest` |
| F2P / P2P | 5 / 208 |
| test files | tests/test_backend/test_slang/test_codegen.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
