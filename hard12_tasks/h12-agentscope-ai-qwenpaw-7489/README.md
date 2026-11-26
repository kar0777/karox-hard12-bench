# HARD12 task `h12-agentscope-ai-qwenpaw-7489`

| item | value |
|---|---|
| source | https://github.com/agentscope-ai/QwenPaw/pull/7489 |
| issue | #7481 (created 2026-09-02) |
| PR created / merged | 2026-09-02 / 2026-09-02 |
| base | `81116f42abaa6a38494950c3defa7e3a1e1d36de` |
| image base | `swerebench/sweb.eval.x86_64.agentscope-ai_1776_qwenpaw-3278:latest` |
| F2P / P2P | 19 / 0 |
| test files | tests/unit/tauri/test_entry.py, tests/unit/tauri/test_pyinstaller_spec.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
