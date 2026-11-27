# HARD12 task `h12-kubeflow-pipelines-13396`

| item | value |
|---|---|
| source | https://github.com/kubeflow/pipelines/pull/13396 |
| issue | #13316 (created 2026-04-24) |
| PR created / merged | 2026-05-14 / 2026-05-26 |
| base | `289267879edc94c7a61ce91cb875ff2acbe28329` |
| image base | `swerebench/sweb.eval.x86_64.kubeflow_1776_pipelines-13112:latest` |
| F2P / P2P | 6 / 49 |
| test files | sdk/python/kfp/dsl/pipeline_task_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
