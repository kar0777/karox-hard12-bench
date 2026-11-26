# HARD12 task `h12-copier-org-copier-2804`

| item | value |
|---|---|
| source | https://github.com/copier-org/copier/pull/2804 |
| issue | #2803 (created 2026-08-11) |
| PR created / merged | 2026-08-11 / 2026-08-21 |
| base | `7f35c79a1c215d49559d9dc55d61a7e3e90ba343` |
| image base | `swerebench/sweb.eval.x86_64.copier-org_1776_copier-2646:latest` |
| F2P / P2P | 1 / 15 |
| test files | tests/test_exclude.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
