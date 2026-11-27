# HARD12 task `h12-aallan-vera-662`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/662 |
| issue | #655 (created 2026-05-11) |
| PR created / merged | 2026-05-12 / 2026-05-12 |
| base | `01281f9c2a0a42e28209a28b956d8e9b308cc10c` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 2 / 1099 |
| test files | tests/test_codegen.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
