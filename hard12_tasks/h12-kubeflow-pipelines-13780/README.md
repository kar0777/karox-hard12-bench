# HARD12 task `h12-kubeflow-pipelines-13780`

| item | value |
|---|---|
| source | https://github.com/kubeflow/pipelines/pull/13780 |
| issue | #11155 (created 2024-08-30) |
| PR created / merged | 2026-07-22 / 2026-07-23 |
| base | `d44866fe914ac3e827cf4e62d2d1560280817205` |
| image base | `swerebench/sweb.eval.x86_64.kubeflow_1776_pipelines-13112:latest` |
| F2P / P2P | 3 / 51 |
| test files | sdk/python/kfp/cli/component_test.py, sdk/python/kfp/dsl/component_factory_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
