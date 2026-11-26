# HARD12 task `h12-microsoft-fabric-cicd-1158`

| item | value |
|---|---|
| source | https://github.com/microsoft/fabric-cicd/pull/1158 |
| issue | #1153 (created 2026-10-07) |
| PR created / merged | 2026-10-11 / 2026-10-13 |
| base | `7f799272f404a4008c3865116dd62f22dbcc36a4` |
| image base | `swerebench/sweb.eval.x86_64.microsoft_1776_fabric-cicd-670:latest` |
| F2P / P2P | 3 / 175 |
| test files | tests/test_fabric_workspace.py, tests/test_parameter_utils.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
