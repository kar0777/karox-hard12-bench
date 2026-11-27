# HARD12 task `h12-aallan-vera-663`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/663 |
| issue | #628 (created 2026-05-08) |
| PR created / merged | 2026-05-12 / 2026-05-12 |
| base | `d22601e0d403c9cb6c2b097e23d96b3d2e01d9c5` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 2 / 19 |
| test files | tests/test_codegen_modules.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
