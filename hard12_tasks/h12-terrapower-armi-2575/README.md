# HARD12 task `h12-terrapower-armi-2575`

| item | value |
|---|---|
| source | https://github.com/terrapower/armi/pull/2575 |
| issue | #1695 (created 2024-04-25) |
| PR created / merged | 2026-07-08 / 2026-07-13 |
| base | `1c149713f90884b85a4074ca4b4c9f49dd793a1c` |
| image base | `swerebench/sweb.eval.x86_64.terrapower_1776_armi-2285:latest` |
| F2P / P2P | 1 / 6 |
| test files | armi/reactor/blueprints/tests/test_componentBlueprint.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
