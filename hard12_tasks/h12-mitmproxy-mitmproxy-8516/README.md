# HARD12 task `h12-mitmproxy-mitmproxy-8516`

| item | value |
|---|---|
| source | https://github.com/mitmproxy/mitmproxy/pull/8516 |
| issue | #8513 (created 2026-10-24) |
| PR created / merged | 2026-10-24 / 2026-10-25 |
| base | `7cb38827580fa8a87af28c43441ab11132747e4a` |
| image base | `swerebench/sweb.eval.x86_64.mitmproxy_1776_mitmproxy-7827:latest` |
| F2P / P2P | 1 / 26 |
| test files | test/mitmproxy/addons/test_tlsconfig.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
