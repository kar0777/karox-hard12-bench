# HARD12 task `h12-brianpugh-cyclopts-954`

| item | value |
|---|---|
| source | https://github.com/BrianPugh/cyclopts/pull/954 |
| issue | #953 (created 2026-09-16) |
| PR created / merged | 2026-09-17 / 2026-09-17 |
| base | `efc7da13c8f9eb88c396ceb151e08d07780616bc` |
| image base | `swerebench/sweb.eval.x86_64.brianpugh_1776_cyclopts-701:latest` |
| F2P / P2P | 24 / 103 |
| test files | tests/config/test_toml_dataclass_list.py, tests/test_json_string_list.py, tests/test_pydantic.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
