# HARD12 task `h12-tox-dev-tox-4094`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/4094 |
| issue | #4093 (created 2026-09-25) |
| PR created / merged | 2026-09-25 / 2026-09-26 |
| base | `9cd0f4e7527e39c30955e31c4307b0630cd37aaa` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 2 / 51 |
| test files | tests/config/test_set_env.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
