# HARD12 task `h12-aallan-vera-1764`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/1764 |
| issue | #1757 (created 2026-10-21) |
| PR created / merged | 2026-10-21 / 2026-10-21 |
| base | `ddada8a9c5b76e8420d53466b0ae4c56cca800e0` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 6 / 72 |
| test files | tests/test_matrix_sample.py, tests/test_trial_argument_labels_1757.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
