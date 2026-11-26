# HARD12 task `h12-terrapower-armi-2630`

| item | value |
|---|---|
| source | https://github.com/terrapower/armi/pull/2630 |
| issue | #2629 (created 2026-08-07) |
| PR created / merged | 2026-08-10 / 2026-08-12 |
| base | `2606abb5f3824aa6425547f03d384bacc23717eb` |
| image base | `swerebench/sweb.eval.x86_64.terrapower_1776_armi-2285:latest` |
| F2P / P2P | 1 / 20 |
| test files | armi/physics/neutronics/globalFlux/tests/test_globalFluxInterface.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
