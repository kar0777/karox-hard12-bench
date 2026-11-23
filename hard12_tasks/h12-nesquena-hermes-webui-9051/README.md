# HARD12 task `h12-nesquena-hermes-webui-9051`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/9051 |
| issue | #9031 (created 2026-11-12) |
| PR created / merged | 2026-11-13 / 2026-11-13 |
| base | `fb6d7afa84369525ec6fb5a3a415b29b3f7c6d3a` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 1 / 2 |
| test files | tests/test_btw_409_lock_scope.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
