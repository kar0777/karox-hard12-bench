# HARD12 task `h12-nesquena-hermes-webui-9203`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/9203 |
| issue | #9149 (created 2026-11-17) |
| PR created / merged | 2026-11-20 / 2026-11-20 |
| base | `9e6c63ae666500fb0b8cca6f57b3f3a52f78fdd5` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 15 / 14 |
| test files | tests/test_issue9149_cached_persistence.py, tests/test_issue9150_bind_hook_boundary.py, tests/test_v050259_sessiondb_fd_leak.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
