# HARD12 task `h12-boxed-mutmut-603`

| item | value |
|---|---|
| source | https://github.com/boxed/mutmut/pull/603 |
| issue | #600 (created 2026-10-13) |
| PR created / merged | 2026-10-16 / 2026-10-19 |
| base | `e687da39dccc3e94aa165f8f5037fe4b24a3a3be` |
| image base | `swerebench/sweb.eval.x86_64.boxed_1776_mutmut-403:latest` |
| F2P / P2P | 1 / 5 |
| test files | tests/mutation/test_mutation_runtime.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
