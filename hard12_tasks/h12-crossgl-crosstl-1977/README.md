# HARD12 task `h12-crossgl-crosstl-1977`

| item | value |
|---|---|
| source | https://github.com/CrossGL/crosstl/pull/1977 |
| issue | #1976 (created 2026-09-30) |
| PR created / merged | 2026-09-30 / 2026-09-30 |
| base | `bd929b665f1445a686d00d0cf6f281f256e7acb9` |
| image base | `swerebench/sweb.eval.x86_64.crossgl_1776_crosstl-257:latest` |
| F2P / P2P | 1 / 15 |
| test files | tests/test_backend/test_metal/test_entry_discovery.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
