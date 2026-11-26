# HARD12 task `h12-nesquena-hermes-webui-6213`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/6213 |
| issue | #6177 (created 2026-07-16) |
| PR created / merged | 2026-07-18 / 2026-07-18 |
| base | `d65c0baf8acac42d7657167a56b2c82a22587982` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 35 / 0 |
| test files | tests/test_api_timeout.py, tests/test_cross_session_message_load_isolation.py, tests/test_issue3162_ensure_messages_loaded.py, tests/test_msg_limit_ceiling_drift.py, tests/test_session_msg_limit_ceiling.py, tests/test_webui_external_refresh_frontend.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
