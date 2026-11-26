# HARD12 task `h12-qbraid-pyqasm-360`

| item | value |
|---|---|
| source | https://github.com/qBraid/pyqasm/pull/360 |
| issue | #354 (created 2026-08-05) |
| PR created / merged | 2026-08-07 / 2026-08-17 |
| base | `40847194cd630b33fbfae5b5d17f23cbc81855fc` |
| image base | `swerebench/sweb.eval.x86_64.qbraid_1776_pyqasm-168:latest` |
| F2P / P2P | 6 / 21 |
| test files | tests/qasm3/test_barrier.py, tests/qasm3/test_measurement.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
