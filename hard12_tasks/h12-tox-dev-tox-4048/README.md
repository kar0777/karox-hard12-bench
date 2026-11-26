# HARD12 task `h12-tox-dev-tox-4048`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/4048 |
| issue | #4047 (created 2026-08-28) |
| PR created / merged | 2026-08-28 / 2026-08-28 |
| base | `930190c1c24106c7dbf75c1ee86f551a0a685e36` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 8 / 25 |
| test files | tests/config/loader/test_loader.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
