# HARD12 task `h12-piskvorky-smart-open-923`

| item | value |
|---|---|
| source | https://github.com/piskvorky/smart_open/pull/923 |
| issue | #712 (created 2022-08-09) |
| PR created / merged | 2026-06-26 / 2026-06-26 |
| base | `5bd8f2bd9595a0524ce62411876b153ccffabae1` |
| image base | `swerebench/sweb.eval.x86_64.piskvorky_1776_smart_open-892:latest` |
| F2P / P2P | 2 / 73 |
| test files | tests/test_azure.py, tests/test_http.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
