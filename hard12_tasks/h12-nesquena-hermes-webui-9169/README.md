# HARD12 task `h12-nesquena-hermes-webui-9169`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/9169 |
| issue | #9167 (created 2026-11-18) |
| PR created / merged | 2026-11-18 / 2026-11-23 |
| base | `b1935597c0402096c578c5cc3fd627f6ff60e68e` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 4 / 2 |
| test files | tests/test_storage_full_error.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
