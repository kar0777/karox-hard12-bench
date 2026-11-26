# HARD12 task `h12-zarr-developers-virtualizarr-1121`

| item | value |
|---|---|
| source | https://github.com/zarr-developers/VirtualiZarr/pull/1121 |
| issue | #1120 (created 2026-10-11) |
| PR created / merged | 2026-10-11 / 2026-10-13 |
| base | `0df56d8432adf7233a4ae1ab70cac3d675a9f654` |
| image base | `swerebench/sweb.eval.x86_64.zarr-developers_1776_virtualizarr-979:latest` |
| F2P / P2P | 8 / 50 |
| test files | virtualizarr/tests/test_parsers/test_hdf/test_hdf.py, virtualizarr/tests/test_writers/test_kerchunk.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
