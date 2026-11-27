# HARD12 task `h12-copier-org-copier-2730`

| item | value |
|---|---|
| source | https://github.com/copier-org/copier/pull/2730 |
| issue | #2729 (created 2026-06-17) |
| PR created / merged | 2026-06-18 / 2026-06-19 |
| base | `b80196e5e075eaa1810323b1dc5836f9698d418b` |
| image base | `swerebench/sweb.eval.x86_64.copier-org_1776_copier-2646:latest` |
| F2P / P2P | 1 / 68 |
| test files | tests/test_updatediff.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
