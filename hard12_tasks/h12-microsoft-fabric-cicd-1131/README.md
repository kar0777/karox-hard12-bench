# HARD12 task `h12-microsoft-fabric-cicd-1131`

| item | value |
|---|---|
| source | https://github.com/microsoft/fabric-cicd/pull/1131 |
| issue | #1129 (created 2026-09-15) |
| PR created / merged | 2026-09-15 / 2026-09-23 |
| base | `8d9e6f8025fff5aba484e4b9ecf331a186ae40f2` |
| image base | `swerebench/sweb.eval.x86_64.microsoft_1776_fabric-cicd-670:latest` |
| F2P / P2P | 14 / 275 |
| test files | tests/test_parameter.py, tests/test_parameter_utils.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
