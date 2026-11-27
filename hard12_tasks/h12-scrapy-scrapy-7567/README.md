# HARD12 task `h12-scrapy-scrapy-7567`

| item | value |
|---|---|
| source | https://github.com/scrapy/scrapy/pull/7567 |
| issue | #4622 (created 2020-06-10) |
| PR created / merged | 2026-06-03 / 2026-06-08 |
| base | `b2d8b06be61df40fd652af2f3fa8238a82b8645d` |
| image base | `swerebench/sweb.eval.x86_64.scrapy_1776_scrapy-7351_interface:latest` |
| F2P / P2P | 6 / 33 |
| test files | tests/test_downloadermiddleware_retry.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
