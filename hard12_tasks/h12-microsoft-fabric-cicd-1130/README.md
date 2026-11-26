# HARD12 task `h12-microsoft-fabric-cicd-1130`

| item | value |
|---|---|
| source | https://github.com/microsoft/fabric-cicd/pull/1130 |
| issue | #1128 (created 2026-09-15) |
| PR created / merged | 2026-09-15 / 2026-09-15 |
| base | `534efeb4800fc0d18df12c49f7900ec98431ac01` |
| image base | `swerebench/sweb.eval.x86_64.microsoft_1776_fabric-cicd-670:latest` |
| F2P / P2P | 1 / 24 |
| test files | tests/test_semantic_model_binding.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
