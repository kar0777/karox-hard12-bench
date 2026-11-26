# HARD12 task `h12-getmoto-moto-10127`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10127 |
| issue | #10126 (created 2026-07-22) |
| PR created / merged | 2026-07-22 / 2026-07-27 |
| base | `115c0a4ddff90ab6a5fb0c2aaffa2282abd981e5` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 1 / 59 |
| test files | tests/test_cloudfront/test_cloudfront_distributions.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
