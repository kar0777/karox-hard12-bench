# HARD12 task `h12-microsoft-fabric-cicd-1178`

| item | value |
|---|---|
| source | https://github.com/microsoft/fabric-cicd/pull/1178 |
| issue | #1174 (created 2026-10-22) |
| PR created / merged | 2026-10-26 / 2026-10-28 |
| base | `a9be0e9f0141029e33ab5545345f928bb7857345` |
| image base | `swerebench/sweb.eval.x86_64.microsoft_1776_fabric-cicd-670:latest` |
| F2P / P2P | 5 / 2 |
| test files | tests/test_base_publisher.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
