# HARD12 task `h12-terrapower-armi-2530`

| item | value |
|---|---|
| source | https://github.com/terrapower/armi/pull/2530 |
| issue | #2525 (created 2026-05-07) |
| PR created / merged | 2026-05-11 / 2026-05-21 |
| base | `f6e8cb9ef4e855258b19773c8da606dd550dd5bf` |
| image base | `swerebench/sweb.eval.x86_64.terrapower_1776_armi-2285:latest` |
| F2P / P2P | 1 / 269 |
| test files | armi/materials/tests/test_materials.py, armi/reactor/blueprints/tests/test_materialModifications.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
