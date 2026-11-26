# HARD12 task `h12-boxed-mutmut-552`

| item | value |
|---|---|
| source | https://github.com/boxed/mutmut/pull/552 |
| issue | #511 (created 2026-04-27) |
| PR created / merged | 2026-08-14 / 2026-08-17 |
| base | `5cb006d3ddeec39d40fb1f2398a77728268b7812` |
| image base | `swerebench/sweb.eval.x86_64.boxed_1776_mutmut-403:latest` |
| F2P / P2P | 21 / 0 |
| test files | tests/mutation/test_trampoline.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
