# HARD12 task `h12-mitmproxy-mitmproxy-8326`

| item | value |
|---|---|
| source | https://github.com/mitmproxy/mitmproxy/pull/8326 |
| issue | #8309 (created 2026-07-04) |
| PR created / merged | 2026-07-16 / 2026-07-17 |
| base | `c8e855310865aca74e634aab840fe5e1b026a938` |
| image base | `swerebench/sweb.eval.x86_64.mitmproxy_1776_mitmproxy-7827:latest` |
| F2P / P2P | 1 / 98 |
| test files | test/mitmproxy/proxy/layers/http/test_http.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
