# HARD12 task `h12-graphistry-pygraphistry-1942`

| item | value |
|---|---|
| source | https://github.com/graphistry/pygraphistry/pull/1942 |
| issue | #1882 (created 2026-08-13) |
| PR created / merged | 2026-08-18 / 2026-08-19 |
| base | `e6625ed28c333dd5c2c0660239de774c489f5198` |
| image base | `swerebench/sweb.eval.x86_64.graphistry_1776_pygraphistry-1277:latest` |
| F2P / P2P | 11 / 7 |
| test files | graphistry/tests/compute/gfql/test_crash_family_1882_1879.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
