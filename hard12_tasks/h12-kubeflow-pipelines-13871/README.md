# HARD12 task `h12-kubeflow-pipelines-13871`

| item | value |
|---|---|
| source | https://github.com/kubeflow/pipelines/pull/13871 |
| issue | #13870 (created 2026-07-26) |
| PR created / merged | 2026-07-26 / 2026-07-29 |
| base | `345a7cd31054d45595322cefe27d73ad7b9f1f10` |
| image base | `swerebench/sweb.eval.x86_64.kubeflow_1776_pipelines-13112:latest` |
| F2P / P2P | 5 / 46 |
| test files | sdk/python/kfp/client/client_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
