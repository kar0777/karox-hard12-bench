# HARD12 task `h12-nesquena-hermes-webui-2865`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/2865 |
| issue | #2845 (created 2026-05-24) |
| PR created / merged | 2026-05-24 / 2026-05-24 |
| base | `59775670358c8cd5f029b747f9ae218845a0e7bf` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 2 / 14 |
| test files | tests/test_default_personality.py, tests/test_issue798.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
