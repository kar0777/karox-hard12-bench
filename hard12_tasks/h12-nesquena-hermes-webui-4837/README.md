# HARD12 task `h12-nesquena-hermes-webui-4837`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/4837 |
| issue | #4768 (created 2026-06-23) |
| PR created / merged | 2026-06-24 / 2026-06-24 |
| base | `853c36724110def4a1d218a76bc158e8b1903e5a` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 1 / 1 |
| test files | tests/test_issue4768_cron_module_missing.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
