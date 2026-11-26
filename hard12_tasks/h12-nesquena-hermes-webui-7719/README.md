# HARD12 task `h12-nesquena-hermes-webui-7719`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/7719 |
| issue | #7710 (created 2026-09-22) |
| PR created / merged | 2026-09-22 / 2026-09-22 |
| base | `b06446cbf5a0e9488ba2dd25d03a3d770b0f19ae` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 12 / 80 |
| test files | tests/test_anchor_scene_persistence.py, tests/test_issue4067_import_cli_cross_profile_guard.py, tests/test_issue4812_session_sse_stream.py, tests/test_issue7710_cross_profile_404_to_409.py, tests/test_session_active_profile_authorization.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
