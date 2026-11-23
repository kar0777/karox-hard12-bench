# HARD12 task `h12-tox-dev-tox-4423`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/4423 |
| issue | #4422 (created 2026-11-12) |
| PR created / merged | 2026-11-12 / 2026-11-17 |
| base | `e1f41591f478c260f71c1f504245cfc75296d48d` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 6 / 150 |
| test files | tests/config/test_set_env.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
