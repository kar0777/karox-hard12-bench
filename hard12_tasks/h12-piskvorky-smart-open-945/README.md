# HARD12 task `h12-piskvorky-smart-open-945`

| item | value |
|---|---|
| source | https://github.com/piskvorky/smart_open/pull/945 |
| issue | #595 (created 2021-03-19) |
| PR created / merged | 2026-06-26 / 2026-06-26 |
| base | `b7081874805d359892c16a15d419b5bc9f33152a` |
| image base | `swerebench/sweb.eval.x86_64.piskvorky_1776_smart_open-892:latest` |
| F2P / P2P | 6 / 175 |
| test files | tests/test_s3_version.py, tests/test_smart_open.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
