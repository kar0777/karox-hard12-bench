# HARD12 task `h12-getmoto-moto-10527`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10527 |
| issue | #10509 (created 2026-10-31) |
| PR created / merged | 2026-11-02 / 2026-11-02 |
| base | `f5af507dcde8445611a0372fc9377d29bdea0597` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 3 / 49 |
| test files | tests/test_s3/test_s3_multipart.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
