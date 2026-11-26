# HARD12 task `h12-beeware-briefcase-2932`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/2932 |
| issue | #2182 (created 2025-03-05) |
| PR created / merged | 2026-07-12 / 2026-07-13 |
| base | `e6f8d8597d4c9a7dce41aa46d4b17fa46b7990a9` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 1 / 5 |
| test files | tests/commands/new/test_build_gui_context.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
