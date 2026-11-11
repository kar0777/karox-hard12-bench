# HARD12 task `h12-beeware-briefcase-3115`

| item | value |
|---|---|
| source | https://github.com/beeware/briefcase/pull/3115 |
| issue | #3113 (created 2026-10-27) |
| PR created / merged | 2026-10-31 / 2026-11-10 |
| base | `ae0eca3d3282fe74c05d966e346c6e1395f435dc` |
| image base | `swerebench/sweb.eval.x86_64.beeware_1776_briefcase-2651:latest` |
| F2P / P2P | 3 / 109 |
| test files | tests/commands/create/test_install_app_support_package.py, tests/commands/create/test_install_stub_binary.py, tests/integrations/file/test_File__download.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
