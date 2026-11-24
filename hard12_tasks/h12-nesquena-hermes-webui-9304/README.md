# HARD12 task `h12-nesquena-hermes-webui-9304`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/9304 |
| issue | #9300 (created 2026-11-23) |
| PR created / merged | 2026-11-23 / 2026-11-23 |
| base | `866a5b8f4c0e940656c0349a36b2825e3272f034` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 1 / 8 |
| test files | tests/test_issue895_894_nous_prefix.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
