# HARD12 task `h12-scrapy-scrapy-7972`

| item | value |
|---|---|
| source | https://github.com/scrapy/scrapy/pull/7972 |
| issue | #4627 (created 2020-06-12) |
| PR created / merged | 2026-08-10 / 2026-08-15 |
| base | `f1694269d8c9437461936ed449e81aa2ccb3b7cb` |
| image base | `swerebench/sweb.eval.x86_64.scrapy_1776_scrapy-7351_interface:latest` |
| F2P / P2P | 1 / 10 |
| test files | tests/test_selector.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
