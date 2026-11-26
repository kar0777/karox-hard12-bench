# HARD12 task `h12-python-wheel-build-fromager-1336`

| item | value |
|---|---|
| source | https://github.com/python-wheel-build/fromager/pull/1336 |
| issue | #1334 (created 2026-09-18) |
| PR created / merged | 2026-09-18 / 2026-09-21 |
| base | `62279db83de85d9161b0a0faf3ff7729c391c229` |
| image base | `swerebench/sweb.eval.x86_64.python-wheel-build_1776_fromager-1124:latest` |
| F2P / P2P | 1 / 53 |
| test files | tests/test_bootstrapper.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
