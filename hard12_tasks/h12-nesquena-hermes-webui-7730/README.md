# HARD12 task `h12-nesquena-hermes-webui-7730`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/7730 |
| issue | #7622 (created 2026-09-17) |
| PR created / merged | 2026-09-22 / 2026-09-23 |
| base | `91044fc18d037166bf786444fe99245749a3dd76` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 1 / 2 |
| test files | tests/test_issue7622_initial_locale_from_browser.py, tests/test_language_precedence.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
