# HARD12 task `h12-crossgl-crosstl-4433`

| item | value |
|---|---|
| source | https://github.com/CrossGL/crosstl/pull/4433 |
| issue | #4428 (created 2026-11-13) |
| PR created / merged | 2026-11-13 / 2026-11-13 |
| base | `ab0f57b52818100ee589b61a768f8365afa7d09b` |
| image base | `swerebench/sweb.eval.x86_64.crossgl_1776_crosstl-257:latest` |
| F2P / P2P | 2 / 287 |
| test files | tests/test_backend/test_directx/test_codegen.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
