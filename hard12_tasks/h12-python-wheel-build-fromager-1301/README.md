# HARD12 task `h12-python-wheel-build-fromager-1301`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1301 |
| issue | #1300 (created 2026-08-10) |
| PR created / merged | 2026-08-10 / 2026-08-11 |
| base | `00f08f87bb4541e7bb0d573e0ad13b4fea458cbd` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 7 / 16 |
| test files | tests/test_vendor_rust.py, tests/test_wheels.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
