# HARD12 task `h12-newton-physics-newton-3744`

| item | value |
|---|---|
| source | https://github.com/newton-physics/newton/pull/3744 |
| issue | #3743 (created 2026-07-31) |
| PR created / merged | 2026-07-31 / 2026-08-18 |
| base | `c29a20583d3658d21b1f218dcc20a8d9a1e3a118` |
| image base | `swerebench/sweb.eval.x86_64.newton-physics_1776_newton-1653:latest` |
| F2P / P2P | 2 / 8 |
| test files | newton/tests/test_mujoco_general_actuators.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
