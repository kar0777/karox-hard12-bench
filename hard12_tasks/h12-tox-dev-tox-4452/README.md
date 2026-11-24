# HARD12 task `h12-tox-dev-tox-4452`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/4452 |
| issue | #4451 (created 2026-11-18) |
| PR created / merged | 2026-11-18 / 2026-11-23 |
| base | `a6a824e8f023a53b7b929287ed2e1fd6a0477f71` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 6 / 54 |
| test files | tests/config/source/test_toml_tox.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
