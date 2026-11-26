You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Advertise supported output formats (available_formats) over the HTTP API

### Summary

Expose the set of output formats a served Tesseract currently accepts (i.e. `tesseract_core.runtime.file_interactions.available_formats()`) over the HTTP API, so a client can discover at runtime whether an experimental format such as `json+cuda_ipc` is available before requesting it.

Today `available_formats()` already computes the answer server-side — `json+cuda_ipc` is included only when `enable_experimental_cuda_ipc` is set — but nothing surfaces it to clients. It is not in the OpenAPI schema and there is no endpoint that returns it.

### Why is this needed?

Downstream libraries (`tesseract-jax`, `tesseract-torch`) can exchange GPU arrays with a served Tesseract via the `json+cuda_ipc` output format, which avoids a host round-trip. Whether that works depends entirely on whether the server was started with `enable_experimental_cuda_ipc=True` — a fact the client cannot currently observe.

Because there is no capability signal, both libraries gate CUDA IPC behind a manual `cuda_ipc=True` argument the user must pass, which is really the user hand-asserting "I know this server opted in." If the assertion is wrong, the request fails (see the companion bug report about the 500). With the capability advertised, the client could enable the fast path automatically when — and only when — the server supports it, and fall back to the host round-trip otherwise. That removes the footgun and lets both libraries drop the manual flag for a transparent UX.

A schema/OpenAPI field is preferable to a dedicated endpoint: clients already fetch `openapi_schema` on connect, so no extra round-trip is needed.

### Usage example

Client-side detection, e.g. in `tesseract-jax` / `tesseract-torch`:

```python
formats = tesseract.supported_output_formats  # newly advertised, from available_formats()
use_cuda_ipc = "json+cuda_ipc" in formats and array.is_cuda
# enable the on-device path automatically, no manual opt-in needed
```

Rough shape of the advertised value:

```json
{"supported_output_formats": ["json", "json+base64", "json+binref", "json+cuda_ipc"]}
```

