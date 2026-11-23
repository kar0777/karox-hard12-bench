# HARD12 task `h12-aallan-vera-1874`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/1874 |
| issue | #909 (created 2026-07-03) |
| PR created / merged | 2026-11-13 / 2026-11-13 |
| base | `9d71d17e24f55ddf599a86d3929b99c3a4eff3d9` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 2 / 118 |
| test files | tests/test_adt_field_facts_909.py, tests/test_build_site.py, tests/test_render_lists.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
