# HARD12 task `h12-aallan-vera-965`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/965 |
| issue | #955 (created 2026-07-08) |
| PR created / merged | 2026-07-09 / 2026-07-09 |
| base | `a835975d326196164c426fa7a2c56c7f404aad43` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 4 / 86 |
| test files | tests/test_diagnostic_fields.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
