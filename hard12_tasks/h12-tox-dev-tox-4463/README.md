# HARD12 task `h12-tox-dev-tox-4463`

| item | value |
|---|---|
| source | https://github.com/tox-dev/tox/pull/4463 |
| issue | #4462 (created 2026-11-23) |
| PR created / merged | 2026-11-23 / 2026-11-23 |
| base | `794908a7f242ef6c82450a9ad7207d3a9bb2fa7f` |
| image base | `swerebench/sweb.eval.x86_64.tox-dev_1776_tox-3931:latest` |
| F2P / P2P | 9 / 294 |
| test files | tests/tox_env/python/pip/req/test_file.py, tests/tox_env/python/pip/test_pip_install.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
