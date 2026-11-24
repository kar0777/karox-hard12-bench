# HARD12 task `h12-newton-physics-newton-5483`

| item | value |
|---|---|
| source | https://github.com/newton-physics/newton/pull/5483 |
| issue | #5391 (created 2026-11-16) |
| PR created / merged | 2026-11-19 / 2026-11-20 |
| base | `d67dbf276618d6d1c4329c0dadfeea6ce6f427d4` |
| image base | `swerebench/sweb.eval.x86_64.newton-physics_1776_newton-1653:latest` |
| F2P / P2P | 18 / 0 |
| test files | newton/tests/test_mujoco_solver.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
