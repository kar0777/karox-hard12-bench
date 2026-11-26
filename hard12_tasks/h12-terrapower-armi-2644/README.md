# HARD12 task `h12-terrapower-armi-2644`

| item | value |
|---|---|
| source | https://github.com/terrapower/armi/pull/2644 |
| issue | #2643 (created 2026-08-26) |
| PR created / merged | 2026-08-27 / 2026-08-27 |
| base | `ce01b794b0f128303adcf6faf072cc1e89e34c59` |
| image base | `swerebench/sweb.eval.x86_64.terrapower_1776_armi-2285:latest` |
| F2P / P2P | 1 / 249 |
| test files | armi/materials/tests/test_materials.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
