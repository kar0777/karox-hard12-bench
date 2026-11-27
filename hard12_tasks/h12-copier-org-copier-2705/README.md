# HARD12 task `h12-copier-org-copier-2705`

| item | value |
|---|---|
| source | https://github.com/copier-org/copier/pull/2705 |
| issue | #2680 (created 2026-05-19) |
| PR created / merged | 2026-05-30 / 2026-06-27 |
| base | `7f09246eff75c5aa7403c1d65bd780d5e8d291bb` |
| image base | `swerebench/sweb.eval.x86_64.copier-org_1776_copier-2646:latest` |
| F2P / P2P | 24 / 329 |
| test files | tests/test_cli.py, tests/test_prompt.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
