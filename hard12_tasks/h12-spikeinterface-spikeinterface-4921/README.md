# HARD12 task `h12-spikeinterface-spikeinterface-4921`

| item | value |
|---|---|
| source | https://github.com/SpikeInterface/spikeinterface/pull/4921 |
| issue | #4915 (created 2026-11-05) |
| PR created / merged | 2026-11-05 / 2026-11-10 |
| base | `4e28d878e240753573ea3e2a42cdf6267015314b` |
| image base | `swerebench/sweb.eval.x86_64.spikeinterface_1776_spikeinterface-3934:latest` |
| F2P / P2P | 6 / 18 |
| test files | src/spikeinterface/core/tests/test_basesorting.py, src/spikeinterface/core/tests/test_numpy_extractors.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
