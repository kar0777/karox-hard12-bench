# HARD12 task `h12-newton-physics-newton-3746`

| item | value |
|---|---|
| source | https://github.com/newton-physics/newton/pull/3746 |
| issue | #3745 (created 2026-07-31) |
| PR created / merged | 2026-07-31 / 2026-08-14 |
| base | `f56650f4c9a589880498f9193d073181b36b2435` |
| image base | `swerebench/sweb.eval.x86_64.newton-physics_1776_newton-1653:latest` |
| F2P / P2P | 5 / 3 |
| test files | newton/tests/test_mujoco_general_actuators.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
