# HARD12 task `h12-idaholab-montepy-1006`

| item | value |
|---|---|
| source | https://github.com/idaholab/MontePy/pull/1006 |
| issue | #982 (created 2026-07-07) |
| PR created / merged | 2026-08-10 / 2026-11-01 |
| base | `ab1ee6138cdd9147f462658da29af1fd558bc1a5` |
| image base | `swerebench/sweb.eval.x86_64.idaholab_1776_montepy-933_interface:latest` |
| F2P / P2P | 2 / 294 |
| test files | tests/test_numbered_collection.py, tests/test_syntax_parsing.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
