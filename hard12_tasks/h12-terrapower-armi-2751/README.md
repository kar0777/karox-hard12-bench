# HARD12 task `h12-terrapower-armi-2751`

| item | value |
|---|---|
| source | https://github.com/terrapower/armi/pull/2751 |
| issue | #2376 (created 2025-12-07) |
| PR created / merged | 2026-11-19 / 2026-11-23 |
| base | `9b69ee925aeef26f67efa35c18efe8237649ac42` |
| image base | `swerebench/sweb.eval.x86_64.terrapower_1776_armi-2285:latest` |
| F2P / P2P | 1 / 14 |
| test files | armi/reactor/blueprints/tests/test_materialModifications.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
