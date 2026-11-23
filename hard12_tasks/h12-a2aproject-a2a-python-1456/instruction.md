You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

[Bug]: SSE client splits data lines on U+2028, U+2029 and U+0085, so streamed events fail to parse

### What happened?

`parse_sse_stream` in `src/a2a/client/transports/http_helpers.py` reads the stream with `response.aiter_lines()` (line 78). httpx's line decoder follows `str.splitlines()`, so it also ends a line at U+2028 (LINE SEPARATOR), U+2029 (PARAGRAPH SEPARATOR) and U+0085 (NEL). SSE line ends are only CR, LF and CRLF, and the docstring on line 73 says the parser conforms to the SSE spec.

The server writes these three characters raw: `json_utils.dumps` uses `ensure_ascii=False` (`src/a2a/utils/json_utils.py:19`). sse-starlette frames on CR/LF only, so it sends one `data:` line. The client splits that line into several. `json.loads` fails on the first piece, and the stream ends with `A2AClientError('Invalid JSON-RPC response in SSE stream')`.

Any string field in a streamed event can hold these characters, for example message text, artifacts or status messages that quote a document. Resubscribing sends the same task snapshot, so that task stays unreadable over streaming. Non-streaming `GetTask` is not affected. The same parser is used by the JSON-RPC and REST transports and by the v0.3 compat transports.

This looks like a regression from #1132, which removed httpx-sse. httpx-sse 0.4.3 split SSE lines on CR/LF only (`_splitlines_sse`).

**Repro** (library level, using the versions pinned in `uv.lock`: sse-starlette 3.4.4, httpx 0.28.1)

```python
import asyncio, json
import httpx
from sse_starlette.sse import ServerSentEvent

async def main():
    data = json.dumps({"text": "before after"}, ensure_ascii=False)
    frame = ServerSentEvent(data=data).encode()
    print(frame.count(b"data:"))  # 1: the server sends one data line
    async def body():
        yield frame
    resp = httpx.Response(200, content=body())
    lines = [l async for l in resp.aiter_lines()]
    print(len(lines))             # 3: the client sees the data line split in two
    json.loads(lines[0][len("data: "):])

asyncio.run(main())
```

Expected: one `data:` line that parses as JSON. Observed: `JSONDecodeError`.

Possible fixes:
- Split SSE lines on CR, LF and CRLF only, with a small line decoder over `aiter_text()`.
- Also, or instead: escape U+2028, U+2029 and U+0085 in `json_utils.dumps`.

Related: #1213, the end-of-stream flush in the same parser.

No existing tests cover these characters in SSE data.

### Relevant log output

```shell
json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 10 (char 9)
```

### Code of Conduct

- [x] I agree to follow this project's Code of Conduct

---
Drafted with Claude Code. I reviewed the code paths and ran the repro.

