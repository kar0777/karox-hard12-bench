# HARD12 task `h12-scrapy-scrapy-8434`

| item | value |
|---|---|
| source | https://github.com/scrapy/scrapy/pull/8434 |
| issue | #8418 (created 2026-10-28) |
| PR created / merged | 2026-10-29 / 2026-11-09 |
| base | `71e4b2b074b38913dbbab671f36a8624954415ac` |
| image base | `swerebench/sweb.eval.x86_64.scrapy_1776_scrapy-7351_interface:latest` |
| F2P / P2P | 2 / 56 |
| test files | tests/test_spider_sitemap.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
