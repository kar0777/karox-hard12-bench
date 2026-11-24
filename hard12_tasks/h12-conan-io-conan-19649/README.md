# HARD12 task `h12-conan-io-conan-19649`

| item | value |
|---|---|
| source | https://github.com/conan-io/conan/pull/19649 |
| issue | #11353 (created 2022-05-27) |
| PR created / merged | 2026-02-20 / 2026-10-26 |
| base | `a5bce6d7b1d4d7676480f883b02db0dc668af5ee` |
| image base | `swerebench/sweb.eval.x86_64.conan-io_1776_conan-19750:latest` |
| F2P / P2P | 3 / 31 |
| test files | test/functional/toolchains/env/test_virtualenv_powershell.py, test/integration/environment/test_env.py, test/integration/environment/test_env_ps1.py, test/integration/environment/test_virtualrunenv_runtime_copy.py, test/integration/toolchains/microsoft/vcvars_test.py |

Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no internet during the agent phase (allowlist = docker bridge only).
