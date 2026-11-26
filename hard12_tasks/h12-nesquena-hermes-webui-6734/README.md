# HARD12 task `h12-nesquena-hermes-webui-6734`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/6734 |
| issue | #6728 (created 2026-08-03) |
| PR created / merged | 2026-08-03 / 2026-08-09 |
| base | `1af7eb5b16742b5adf67ce4dfe16cac685f63643` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 2 / 19 |
| test files | tests/test_6728_cron_running_sidebar.py, tests/test_issue856_background_completion_unread.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
