# HARD12 task `h12-pasteurlabs-tesseract-core-802`

| item | value |
|---|---|
| source | https://github.com/pasteurlabs/tesseract-core/pull/802 |
| issue | #801 (created 2026-09-28) |
| PR created / merged | 2026-09-28 / 2026-10-05 |
| base | `6f202d0a55dbfc0667048eab763ccd507aa17035` |
| image base | `swerebench/sweb.eval.x86_64.pasteurlabs_1776_tesseract-core-302:latest` |
| F2P / P2P | 21 / 0 |
| test files | tests/runtime_tests/test_jax_recipes.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
