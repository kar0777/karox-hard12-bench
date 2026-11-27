# HARD12 task `h12-scrapy-scrapy-7694`

| item | value |
|---|---|
| source | https://github.com/scrapy/scrapy/pull/7694 |
| issue | #7015 (created 2025-08-22) |
| PR created / merged | 2026-06-29 / 2026-06-30 |
| base | `4b2b56f3848111d55151ccfefddfc6b3d84d1302` |
| image base | `swerebench/sweb.eval.x86_64.scrapy_1776_scrapy-7351_interface:latest` |
| F2P / P2P | 3 / 59 |
| test files | tests/test_feedexport.py, tests/test_item.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
