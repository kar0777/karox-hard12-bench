# HARD12 task `h12-copier-org-copier-2686`

| item | value |
|---|---|
| source | https://github.com/copier-org/copier/pull/2686 |
| issue | #2267 (created 2025-08-08) |
| PR created / merged | 2026-05-22 / 2026-05-24 |
| base | `659f4e85c47bb74f5ae51e0d34b22cdbfa488f81` |
| image base | `swerebench/sweb.eval.x86_64.copier-org_1776_copier-2646:latest` |
| F2P / P2P | 3 / 208 |
| test files | tests/test_copy.py, tests/test_dynamic_file_structures.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
