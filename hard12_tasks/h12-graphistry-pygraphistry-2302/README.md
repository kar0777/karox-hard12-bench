# HARD12 task `h12-graphistry-pygraphistry-2302`

| item | value |
|---|---|
| source | https://github.com/graphistry/pygraphistry/pull/2302 |
| issue | #2277 (created 2026-11-07) |
| PR created / merged | 2026-11-12 / 2026-11-12 |
| base | `2fe4dc01177ea7bf4d85f9118d1f65eb84e59509` |
| image base | `swerebench/sweb.eval.x86_64.graphistry_1776_pygraphistry-1277:latest` |
| F2P / P2P | 29 / 27 |
| test files | graphistry/tests/compute/test_chain_remote_v2.py, graphistry/tests/compute/test_remote_cypher_lossless.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
