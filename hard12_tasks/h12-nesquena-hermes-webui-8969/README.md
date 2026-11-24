# HARD12 task `h12-nesquena-hermes-webui-8969`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/8969 |
| issue | #8862 (created 2026-11-05) |
| PR created / merged | 2026-11-09 / 2026-11-10 |
| base | `668cf1c0c87bd0dfb7f4d6e5d74fa83e5e9da0b5` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 6 / 3 |
| test files | tests/test_issue8862_session_new_invalid_profile.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
