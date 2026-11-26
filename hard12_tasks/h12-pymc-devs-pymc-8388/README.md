# HARD12 task `h12-pymc-devs-pymc-8388`

| item | value |
|---|---|
| source | https://github.com/pymc-devs/pymc/pull/8388 |
| issue | #8386 (created 2026-08-02) |
| PR created / merged | 2026-08-03 / 2026-08-03 |
| base | `9e94b4868dfb3aec26414ebafb1603a65c774855` |
| image base | `swerebench/sweb.eval.x86_64.pymc-devs_1776_pymc-7858:latest` |
| F2P / P2P | 3 / 55 |
| test files | tests/distributions/test_censored.py, tests/logprob/test_censoring.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
