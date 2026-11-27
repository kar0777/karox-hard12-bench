# HARD12 task `h12-tox-dev-tox-3948`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/3948 |
| issue | #3945 (created 2026-05-19) |
| PR created / merged | 2026-05-28 / 2026-05-28 |
| base | `27b68b39e6db707909311e654fcb6aa4d626cccf` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 2 / 50 |
| test files | tests/tox_env/python/pip/test_pip_install.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
