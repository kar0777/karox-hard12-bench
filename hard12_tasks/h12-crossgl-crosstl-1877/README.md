# HARD12 task `h12-crossgl-crosstl-1877`

| item | value |
|---|---|
| source | https://github.com/CrossGL/crosstl/pull/1877 |
| issue | #1519 (created 2026-07-11) |
| PR created / merged | 2026-08-02 / 2026-08-11 |
| base | `bb2305b6d5dbb6399c096919b18af433696fd138` |
| image base | `swerebench/sweb.eval.x86_64.crossgl_1776_crosstl-257:latest` |
| F2P / P2P | 2 / 1185 |
| test files | tests/test_translator/test_codegen/test_directx_codegen.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
