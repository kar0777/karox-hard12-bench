# HARD12 task `h12-terrapower-armi-2699`

| item | value |
|---|---|
| source | https://github.com/terrapower/armi/pull/2699 |
| issue | #2697 (created 2026-10-14) |
| PR created / merged | 2026-10-14 / 2026-10-14 |
| base | `fdeb761334f39ba1cda37d0a5260d3ee8b866c99` |
| image base | `swerebench/sweb.eval.x86_64.terrapower_1776_armi-2285:latest` |
| F2P / P2P | 1 / 19 |
| test files | armi/physics/neutronics/latticePhysics/tests/test_latticeInterface.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
