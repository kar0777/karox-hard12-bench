# HARD12 task `h12-pdm-project-pdm-4001`

| item | value |
|---|---|
| source | https://github.com/pdm-project/pdm/pull/4001 |
| issue | #4000 (created 2026-11-08) |
| PR created / merged | 2026-11-08 / 2026-11-10 |
| base | `2c33691a1b87dbe05190df69971c8053da32ac3f` |
| image base | `swerebench/sweb.eval.x86_64.pdm-project_1776_pdm-3759:latest` |
| F2P / P2P | 3 / 43 |
| test files | tests/models/test_candidates.py, tests/models/test_session.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
