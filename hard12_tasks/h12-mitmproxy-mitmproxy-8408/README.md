# HARD12 task `h12-mitmproxy-mitmproxy-8408`

| item | value |
|---|---|
| source | https://github.com/mitmproxy/mitmproxy/pull/8408 |
| issue | #8407 (created 2026-08-27) |
| PR created / merged | 2026-08-29 / 2026-09-10 |
| base | `2ac5b089d953585c66026a53f678270e094e48e5` |
| image base | `swerebench/sweb.eval.x86_64.mitmproxy_1776_mitmproxy-7827:latest` |
| F2P / P2P | 2 / 8 |
| test files | test/mitmproxy/addons/test_browser.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
