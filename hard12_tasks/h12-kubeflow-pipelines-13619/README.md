# HARD12 task `h12-kubeflow-pipelines-13619`

| item | value |
|---|---|
| source | https://github.com/kubeflow/pipelines/pull/13619 |
| issue | #13420 (created 2026-05-20) |
| PR created / merged | 2026-07-01 / 2026-09-06 |
| base | `2c9c19cd454568180f2d6710627334528214c461` |
| image base | `swerebench/sweb.eval.x86_64.kubeflow_1776_pipelines-13112:latest` |
| F2P / P2P | 1 / 51 |
| test files | sdk/python/kfp/dsl/structures_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
