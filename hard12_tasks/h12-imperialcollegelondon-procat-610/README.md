# HARD12 task `h12-imperialcollegelondon-procat-610`

| item | value |
|---|---|
| source | https://github.com/ImperialCollegeLondon/proCAT/pull/610 |
| issue | #519 (created 2026-01-09) |
| PR created / merged | 2026-04-28 / 2026-05-12 |
| base | `07d17e589d8073f428bc3539030c4b4a0b2358ad` |
| image base | `swerebench/sweb.eval.x86_64.imperialcollegelondon_1776_procat-503:latest` |
| F2P / P2P | 1 / 70 |
| test files | tests/main/test_models.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
