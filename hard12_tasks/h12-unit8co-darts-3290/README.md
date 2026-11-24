# HARD12 task `h12-unit8co-darts-3290`

| item | value |
|---|---|
| source | https://github.com/unit8co/darts/pull/3290 |
| issue | #3276 (created 2026-10-16) |
| PR created / merged | 2026-10-24 / 2026-10-28 |
| base | `0880bfff1bd56290f6b525b452836011e76326bc` |
| image base | `swerebench/sweb.eval.x86_64.unit8co_1776_darts-3065:latest` |
| F2P / P2P | 2 / 6 |
| test files | darts/tests/test_logging.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
