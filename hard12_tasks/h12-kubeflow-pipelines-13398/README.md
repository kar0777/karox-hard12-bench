# HARD12 task `h12-kubeflow-pipelines-13398`

| item | value |
|---|---|
| source | https://github.com/kubeflow/pipelines/pull/13398 |
| issue | #11038 (created 2024-07-25) |
| PR created / merged | 2026-05-15 / 2026-05-15 |
| base | `2582d6be7fe41333d26e0dd68e2a15818f7f1d30` |
| image base | `swerebench/sweb.eval.x86_64.kubeflow_1776_pipelines-13112:latest` |
| F2P / P2P | 1 / 28 |
| test files | sdk/python/kfp/cli/component_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
