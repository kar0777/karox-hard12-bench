# HARD12 task `h12-aallan-vera-1826`

| item | value |
|---|---|
| source | https://github.com/aallan/vera/pull/1826 |
| issue | #1822 (created 2026-10-31) |
| PR created / merged | 2026-11-02 / 2026-11-02 |
| base | `0c334c8ad01d5bba84b3fe4a474ffac0219184d9` |
| image base | `swerebench/sweb.eval.x86_64.aallan_1776_vera-662_interface:latest` |
| F2P / P2P | 4 / 443 |
| test files | tests/program_generator.py, tests/test_composite_coercion_guards.py, tests/test_distrust_corpus.py, tests/test_mutate_diff.py, tests/test_program_generator.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
