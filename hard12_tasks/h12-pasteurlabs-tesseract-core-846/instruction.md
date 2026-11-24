You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Point the generic HTTP 500 from a served Tesseract to debug mode

When an endpoint raises, a served Tesseract responds with a bare `500 Internal Server Error`. Keeping tracebacks out of responses is deliberate, since exposing them would be unsafe in production. The traceback still goes to the server log, and debug mode (`tesseract serve --debug`, or `TESSERACT_DEBUG=1`) includes it in the response. The response mentions neither of these, though.

Feedback from hackathon participants suggests this costs real time. Unrelated bugs look identical from the client side, and people (and their coding agents) didn't find debug mode, even though the debugging guide documents it.

To reproduce:

```python
# tesseract_api.py
from pydantic import BaseModel

class InputSchema(BaseModel):
    x: float

class OutputSchema(BaseModel):
    y: float

def apply(inputs: InputSchema) -> OutputSchema:
    raise ValueError("boom")
```

```console
$ TESSERACT_API_PATH=tesseract_api.py tesseract-runtime serve --port 8000
$ curl -X POST localhost:8000/apply -H 'content-type: application/json' -d '{"inputs": {"x": 1}}'
Internal Server Error
```

Through the SDK, this surfaces as `RuntimeError: Error 500 from Tesseract: Internal Server Error`.

## Proposal

- **Runtime.** Outside debug mode, return a 500 whose body names the next step, for example: "Internal server error. The traceback is in the server log. Enable debug mode (`TESSERACT_DEBUG=1`, or `tesseract serve --debug`) to include it in responses." Leave debug mode unchanged. Since `serve.py` registers no handler for unhandled exceptions, the current body is the framework's default.
- **SDK.** When `_decode_response` gets a 500, add the same hint to the `RuntimeError`, so clients get it from runtimes that predate the change too (see #823).

## Open question

The right flag depends on how the Tesseract was started (`tesseract serve`, `tesseract-runtime serve`, `Tesseract.from_source`, a remote URL). One message that is correct for all of them probably has to name the environment variable and link the debugging guide, rather than spell out every variant.

