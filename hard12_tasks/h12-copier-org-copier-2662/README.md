# HARD12 task `h12-copier-org-copier-2662`

| item | value |
|---|---|
| source | https://github.com/copier-org/copier/pull/2662 |
| issue | #2126 (created 2025-05-05) |
| PR created / merged | 2026-05-10 / 2026-05-12 |
| base | `e706e813d9bfe4b06cbd91b4196bc6fc456f9764` |
| image base | `swerebench/sweb.eval.x86_64.copier-org_1776_copier-2646:latest` |
| F2P / P2P | 7 / 195 |
| test files | tests/test_copy.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
