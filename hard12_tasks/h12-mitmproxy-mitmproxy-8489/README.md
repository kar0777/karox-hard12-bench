# HARD12 task `h12-mitmproxy-mitmproxy-8489`

| item | value |
|---|---|
| source | https://github.com/mitmproxy/mitmproxy/pull/8489 |
| issue | #8488 (created 2026-10-17) |
| PR created / merged | 2026-10-17 / 2026-10-20 |
| base | `f9c59ef5243dd24e53e2b6e57c4fff64bc09f7c4` |
| image base | `swerebench/sweb.eval.x86_64.mitmproxy_1776_mitmproxy-7827:latest` |
| F2P / P2P | 1 / 10 |
| test files | test/mitmproxy/net/http/test_cookies.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
