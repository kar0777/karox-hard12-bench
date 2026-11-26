# HARD12 task `h12-scrapy-scrapy-8192`

| item | value |
|---|---|
| source | https://github.com/scrapy/scrapy/pull/8192 |
| issue | #2592 (created 2017-02-23) |
| PR created / merged | 2026-09-21 / 2026-09-21 |
| base | `b6ac7852a2aaea3d8512aba6062dbc271ea90dcb` |
| image base | `swerebench/sweb.eval.x86_64.scrapy_1776_scrapy-7351_interface:latest` |
| F2P / P2P | 2 / 19 |
| test files | tests/test_http_headers.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
