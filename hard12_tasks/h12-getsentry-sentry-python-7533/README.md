# HARD12 task `h12-getsentry-sentry-python-7533`

| item | value |
|---|---|
| source | https://github.com/getsentry/sentry-python/pull/7533 |
| issue | #6094 (created 2026-04-19) |
| PR created / merged | 2026-09-17 / 2026-10-05 |
| base | `185fb9c219786fa1b7082dfd207b6c1f3d44ad8c` |
| image base | `swerebench/sweb.eval.x86_64.getsentry_1776_sentry-python-4231:latest` |
| F2P / P2P | 1 / 102 |
| test files | tests/test_basics.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
