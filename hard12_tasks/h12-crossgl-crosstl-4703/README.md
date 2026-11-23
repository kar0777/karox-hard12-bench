# HARD12 task `h12-crossgl-crosstl-4703`

| item | value |
|---|---|
| source | https://github.com/CrossGL/crosstl/pull/4703 |
| issue | #4699 (created 2026-11-20) |
| PR created / merged | 2026-11-20 / 2026-11-21 |
| base | `1ebda13cf0f07f805760975d7fab055ef0fd0475` |
| image base | `swerebench/sweb.eval.x86_64.crossgl_1776_crosstl-257:latest` |
| F2P / P2P | 1 / 16 |
| test files | tests/test_backend/test_OpenCL/test_sizeof_and_refusals.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
