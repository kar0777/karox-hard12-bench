# HARD12 task `h12-nesquena-hermes-webui-9013`

| item | value |
|---|---|
| source | https://github.com/nesquena/hermes-webui/pull/9013 |
| issue | #8869 (created 2026-11-05) |
| PR created / merged | 2026-11-11 / 2026-11-11 |
| base | `1a0f2714d9f245afd89d93b9c1ee94f512036d77` |
| image base | `swerebench/sweb.eval.x86_64.nesquena_1776_hermes-webui-2056:latest` |
| F2P / P2P | 3 / 3 |
| test files | tests/test_issue9000_sibling_paths.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
