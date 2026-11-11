# HARD12 task `h12-scipp-plopp-614`

| item | value |
|---|---|
| source | https://github.com/scipp/plopp/pull/614 |
| issue | #613 (created 2026-10-21) |
| PR created / merged | 2026-10-23 / 2026-10-28 |
| base | `57b5af5a7c1c1451696c925b41cd97df969ca0c6` |
| image base | `swerebench/sweb.eval.x86_64.scipp_1776_plopp-513:latest` |
| F2P / P2P | 17 / 47 |
| test files | tests/backends/matplotlib/mpl_image_test.py, tests/graphics/colormapper_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
