# HARD12 task `h12-microsoft-fabric-cicd-1165`

| item | value |
|---|---|
| source | https://github.com/microsoft/fabric-cicd/pull/1165 |
| issue | #1163 (created 2026-10-15) |
| PR created / merged | 2026-10-15 / 2026-10-19 |
| base | `e0d20cc167ca4dc1a380c5a91644b751eadfdcea` |
| image base | `swerebench/sweb.eval.x86_64.microsoft_1776_fabric-cicd-670:latest` |
| F2P / P2P | 5 / 16 |
| test files | tests/test_datapipeline_dependencies.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
