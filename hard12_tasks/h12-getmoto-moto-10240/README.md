# HARD12 task `h12-getmoto-moto-10240`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10240 |
| issue | #10239 (created 2026-09-05) |
| PR created / merged | 2026-09-05 / 2026-09-07 |
| base | `f940cfd7942af2abf952de35337b14bdba208e9c` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 1 / 5 |
| test files | tests/test_s3control/test_s3control_access_points.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
