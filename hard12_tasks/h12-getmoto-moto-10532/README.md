# HARD12 task `h12-getmoto-moto-10532`

| item | value |
|---|---|
| source | https://github.com/getmoto/moto/pull/10532 |
| issue | #10422 (created 2026-10-23) |
| PR created / merged | 2026-11-03 / 2026-11-03 |
| base | `7c5e18448556954aa1220a710c8b6a11654ddf22` |
| image base | `swerebench/sweb.eval.x86_64.getmoto_1776_moto-9903:latest` |
| F2P / P2P | 2 / 35 |
| test files | tests/test_ec2/test_launch_templates.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
