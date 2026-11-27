# HARD12 task `h12-microsoft-fabric-cicd-1057`

| item | value |
|---|---|
| source | https://github.com/microsoft/fabric-cicd/pull/1057 |
| issue | #1044 (created 2026-06-25) |
| PR created / merged | 2026-07-08 / 2026-07-09 |
| base | `5b90568ef1a043e702c895d5cb4f3690355ff1b0` |
| image base | `swerebench/sweb.eval.x86_64.microsoft_1776_fabric-cicd-670:latest` |
| F2P / P2P | 3 / 92 |
| test files | tests/test_parameter_utils.py, tests/test_subfolders.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
