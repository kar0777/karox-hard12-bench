# HARD12 task `h12-nesquena-hermes-webui-8877`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/8877 |
| issue | #8852 (created 2026-11-05) |
| PR created / merged | 2026-11-06 / 2026-11-06 |
| base | `52e95f229405185288cedd7ef1b1ceb5fb1f3442` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 16 / 10 |
| test files | tests/test_issue8852_body_id_write_target.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
