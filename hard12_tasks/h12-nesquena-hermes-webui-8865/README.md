# HARD12 task `h12-nesquena-hermes-webui-8865`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/8865 |
| issue | #8837 (created 2026-11-05) |
| PR created / merged | 2026-11-05 / 2026-11-06 |
| base | `f65960b46351815958e8ce5e0f81585a5764531b` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 17 / 22 |
| test files | tests/test_issue8399_share_revocation.py, tests/test_issue8837_share_outlives_delete.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
