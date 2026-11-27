# HARD12 task `h12-imperialcollegelondon-procat-608`

| item | value |
|---|---|
| source | https://github.com/ImperialCollegeLondon/proCAT/pull/608 |
| issue | #597 (created 2026-04-14) |
| PR created / merged | 2026-04-27 / 2026-05-12 |
| base | `c388244a95df3204b04646f29dc9bd080c153de8` |
| image base | `swerebench/sweb.eval.x86_64.imperialcollegelondon_1776_procat-503:latest` |
| F2P / P2P | 5 / 79 |
| test files | tests/main/test_models.py, tests/main/test_report.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
