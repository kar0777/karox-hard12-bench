You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Model picker in chatbar only shows configured default model — other providers and models are invisible

The model picker dropdown in the webui chatbar should list all available models across all detected providers. Instead, it only shows the single configured default model — users cannot see or select any other models from any other provider.

`hermes model` from the CLI shows the full list of providers and models, confirming the agent itself is working correctly. The problem is isolated to the webui model picker.

## Steps to reproduce

1. Run the webui (`hermes dashboard` or `python run.py`)
2. Open the chatbar and click the model picker (model chip in the composer footer)
3. Observe that only one model is listed (the configured default)
4. Run `hermes model` from the CLI — the full list of providers/models is shown there

## Expected

The picker shows all detected providers with their model lists.

## Actual

The picker shows only one model (the configured default).

## Environment

- hermes-webui version: v0.51.350
- OS: Ubuntu 24.x

## Possible location of the issue

The model picker data comes from `GET /api/models`, served by `api/config.py::get_available_models()`. That function builds a `detected_providers` set, then for each provider builds its model group. If `detected_providers` ends up empty or incomplete, the function falls through to a fallback that appends only the single `default_model` entry under a "Default" group — which is what the user sees.

The CLI `hermes model` uses `hermes_cli/models.py` directly, which has broader provider/model detection via `build_models_payload(include_unconfigured=True)`. This suggests the detection logic in `get_available_models()` may be missing providers that the CLI catches, or hitting an empty path for certain provider types.
