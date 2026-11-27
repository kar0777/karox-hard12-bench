# HARD12 task `h12-mitmproxy-mitmproxy-8203`

| item | value |
|---|---|
| source | https://github.com/mitmproxy/mitmproxy/pull/8203 |
| issue | #8201 (created 2026-04-30) |
| PR created / merged | 2026-05-01 / 2026-05-11 |
| base | `b464cbf82308547f461a916b18db96d05c399944` |
| image base | `swerebench/sweb.eval.x86_64.mitmproxy_1776_mitmproxy-7827:latest` |
| F2P / P2P | 1 / 36 |
| test files | test/mitmproxy/test_certs.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
