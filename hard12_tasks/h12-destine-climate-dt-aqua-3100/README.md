# HARD12 task `h12-destine-climate-dt-aqua-3100`

| item | value |
|---|---|
| source | https://github.com/DestinE-Climate-DT/AQUA/pull/3100 |
| issue | #3098 (created 2026-09-18) |
| PR created / merged | 2026-09-18 / 2026-09-25 |
| base | `f13e66c49bf2f6b91c81811ae0925625768f34b5` |
| image base | `swerebench/sweb.eval.x86_64.destine-climate-dt_1776_aqua-2768:latest` |
| F2P / P2P | 3 / 6 |
| test files | tests/test_gsv.py, tests/test_z3fdb_opener.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
