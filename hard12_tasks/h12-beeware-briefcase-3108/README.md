# HARD12 task `h12-beeware-briefcase-3108`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/3108 |
| issue | #1634 (created 2024-02-04) |
| PR created / merged | 2026-10-26 / 2026-10-28 |
| base | `65172382060f4cd359fcb283e1acb227de09bf3e` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 1 / 21 |
| test files | tests/integrations/docker/test_Docker__verify.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
