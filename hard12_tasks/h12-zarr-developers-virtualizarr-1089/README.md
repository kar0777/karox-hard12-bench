# HARD12 task `h12-zarr-developers-virtualizarr-1089`

| item | value |
|---|---|
| source | https://github.com/zarr-developers/VirtualiZarr/pull/1089 |
| issue | #1088 (created 2026-08-14) |
| PR created / merged | 2026-08-17 / 2026-10-14 |
| base | `adcdea798b93575f9cc73a1d594ed575c2f75e56` |
| image base | `swerebench/sweb.eval.x86_64.zarr-developers_1776_virtualizarr-979:latest` |
| F2P / P2P | 7 / 51 |
| test files | conftest.py, virtualizarr/tests/test_manifests/test_manifest.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
