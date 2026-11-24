# HARD12 task `h12-scrapy-scrapy-8386`

| item | value |
|---|---|
| source | https://github.com/scrapy/scrapy/pull/8386 |
| issue | #8297 (created 2026-10-09) |
| PR created / merged | 2026-10-21 / 2026-10-21 |
| base | `ca5f3c1acf430429563485997e207661d24b11da` |
| image base | `swerebench/sweb.eval.x86_64.scrapy_1776_scrapy-7351_interface:latest` |
| F2P / P2P | 3 / 22 |
| test files | tests/test_downloadermiddleware_robotstxt.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
