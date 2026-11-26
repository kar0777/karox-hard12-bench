# HARD12 task `h12-nesquena-hermes-webui-8084`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/8084 |
| issue | #7945 (created 2026-10-01) |
| PR created / merged | 2026-10-08 / 2026-10-08 |
| base | `0595825cb40bb92913716932bcf4eb96ada3b840` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 9 / 23 |
| test files | tests/test_issue3831_watermark_clear.py, tests/test_stale_watermark_self_heal.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
