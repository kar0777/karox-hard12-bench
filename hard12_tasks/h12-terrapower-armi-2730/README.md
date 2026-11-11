# HARD12 task `h12-terrapower-armi-2730`

| item | value |
|---|---|
| source | https://github.com/terrapower/armi/pull/2730 |
| issue | #2717 (created 2026-10-28) |
| PR created / merged | 2026-11-04 / 2026-11-10 |
| base | `5fd928b5868328ec02b0a1bc854becffe5de4899` |
| image base | `swerebench/sweb.eval.x86_64.terrapower_1776_armi-2285:latest` |
| F2P / P2P | 5 / 109 |
| test files | armi/physics/neutronics/tests/test_crossSectionManager.py, armi/reactor/tests/test_assemblies.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
