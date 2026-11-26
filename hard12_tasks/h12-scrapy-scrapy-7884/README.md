# HARD12 task `h12-scrapy-scrapy-7884`

| item | value |
|---|---|
| source | https://github.com/scrapy/scrapy/pull/7884 |
| issue | #3463 (created 2018-10-15) |
| PR created / merged | 2026-08-05 / 2026-08-09 |
| base | `a6c017c2ca2b8a9bca8b46b692846f492fe77a00` |
| image base | `swerebench/sweb.eval.x86_64.scrapy_1776_scrapy-7351_interface:latest` |
| F2P / P2P | 3 / 82 |
| test files | tests/test_crawler_subprocess.py, tests/test_engine_loop.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
