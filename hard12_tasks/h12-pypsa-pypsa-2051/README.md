# HARD12 task `h12-pypsa-pypsa-2051`

| item | value |
|---|---|
| source | https://github.com/PyPSA/PyPSA/pull/2051 |
| issue | #2020 (created 2026-10-20) |
| PR created / merged | 2026-10-28 / 2026-11-02 |
| base | `23650353eb1d059acfec28f4915ad3e068c085bf` |
| image base | `swerebench/sweb.eval.x86_64.pypsa_1776_pypsa-1653:latest` |
| F2P / P2P | 4 / 55 |
| test files | test/test_lopf_unit_commitment.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
