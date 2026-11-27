You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Streaming drops all deltas when model emits <tool_call> markup on Qwen3.6-35B-A3B (v0.6.61, qwen3_xml + --no-thinking); non-streaming returns valid tool_calls

### Rapid-MLX version

0.6.61 (uv tool install)

### Hardware

MacBook Pro M4 Pro, 48 GB

### macOS version

26.2 (Darwin 25.2.0)

### Python version

3.13.13 (uv-managed venv at `~/.local/share/uv/tools/rapid-mlx`)

### Model

`mlx-community/Qwen3.6-35B-A3B-4bit-DWQ`

### Full serve command

```
rapid-mlx serve mlx-community/Qwen3.6-35B-A3B-4bit-DWQ \
  --port 8001 \
  --prefill-step-size 8192 \
  --reasoning-parser qwen3 \
  --tool-call-parser qwen3_xml \
  --enable-auto-tool-choice \
  --served-model-name qwen3.6-35b-mlx \
  --gpu-memory-utilization 1.0 \
  --kv-cache-quantization \
  --kv-cache-quantization-bits 8 \
  --no-thinking
```

### What happens

Whenever the model emits `<tool_call>...</tool_call>` markup in streaming mode, the entire response is dropped on the wire. The stream emits exactly two SSE events — a role opener and a `finish_reason: stop` closer — with `completion_tokens` correctly accounting for the generated tokens, but zero `content`, `reasoning_content`, or `tool_calls` deltas.

The same prompt non-streaming returns a clean parsed `tool_calls` array with `finish_reason: tool_calls`. So the model + parser are doing the right thing; only the streaming wire path is broken.

This is independent of:

- `--no-thinking` vs `--reasoning-parser qwen3` alone (both fail; with reasoning enabled the tool call gets gobbled into `reasoning_content` as 215 deltas of think-block text, then a single `"\n\n"` content delta — also broken, possibly the same root cause as the still-open #344)
- `tool_choice: "auto"` vs `tool_choice: "none"`
- whether `tools: [...]` is set in the request at all — the parser still extracts and drops the tool call

The 0.6.61 finalize-fallback in `service/postprocessor.py:510` does ship in this install (verified — line 510 has the `"[Calling"` substring check, line 518 invokes `extract_tool_calls`), and the substring `"<"` in the response should trigger it. It does not. Either `_fallback_text` is empty by the time finalize runs (qwen3_xml parser consumed tokens without surfacing them to fallback), or the fallback path runs but the resulting tool_call event isn't getting written to the SSE stream.

### Reproduction

Server up (command above). Streaming request:

```
curl -sN -i http://127.0.0.1:8001/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3.6-35b-mlx",
    "messages": [{"role":"user","content":"Read /etc/hostname"}],
    "tools": [{"type":"function","function":{"name":"read_file","description":"Read a file","parameters":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}}}],
    "tool_choice": "auto",
    "max_tokens": 200,
    "temperature": 0,
    "stream": true
  }'
```

Full wire response (verbatim, every byte):

```
HTTP/1.1 200 OK
content-type: text/event-stream; charset=utf-8

data: {"id":"chatcmpl-df245252","object":"chat.completion.chunk","created":...,"choices":[{"index":0,"delta":{"role":"assistant"}}]}

data: {"id":"chatcmpl-df245252","object":"chat.completion.chunk","created":...,"choices":[{"index":0,"delta":{},"finish_reason":"stop"}],"usage":{"prompt_tokens":358,"completion_tokens":27,"total_tokens":385}}

data: [DONE]
```

Server-side log for that same request:

```
[REQUEST] POST /v1/chat/completions stream=True ... tools=1
[stream_outputs] ... first token after 0.8s
[stream_outputs] ... finished normally, 27 tokens in 1.2s
Chat completion (stream): 27 tokens in 1.28s (21.1 tok/s)
```

27 tokens generated. Stream emitted 0 deltas.

### Same prompt non-streaming (works)

Drop `"stream": true`:

```json
{
  "finish_reason": "tool_calls",
  "usage": {"prompt_tokens": 358, "completion_tokens": 27, "total_tokens": 385},
  "message": {
    "tool_calls": [{
      "id": "call_0f3795d5",
      "type": "function",
      "function": {"name": "read_file", "arguments": "{\"path\": \"/etc/hostname\"}"}
    }]
  }
}
```

Identical model behaviour (same 27 tokens), parser extracts correctly.

### Isolation tests

| Streaming request | Result |
|---|---|
| `What is the capital of France?` + tools in request, `tool_choice: auto` | streams "Paris" cleanly |
| `Read /etc/hostname` + tools, `tool_choice: auto` | 0 deltas, finish_reason: stop, 27 tokens generated |
| `Read /etc/hostname` + tools, `tool_choice: none` | 0 deltas (model still emits `<tool_call>`, gets eaten anyway) |
| `Read /etc/hostname` + no tools at all in request | 0 deltas (model still emits `<tool_call>`, parser still extracts and drops) |
| Plain prompt asking to print literal `hello <stuff> world` | streams `hello <stuff> world` cleanly (so it's not "any angle bracket triggers it") |
| Plain prompt asking to print literal `<tool_call>FAKE</tool_call> end` | model refuses ("XML entity injection attempt") — separate behaviour, ignore |

The trigger is the model emitting `<tool_call>` markup, not the request shape.

### Expected

Streamed `tool_calls` deltas + `finish_reason: tool_calls` (same as non-streaming).

### Related

- #344 (open): tool_call inside `<think>` blocks gets classified as reasoning. The reasoning-enabled streaming behaviour above (215 reasoning deltas, `<tool_call>` swallowed) looks like the same root cause as #344. The `--no-thinking` case in this report is different — there's no `<think>` block at all, the model jumps straight to `<tool_call>` and it still gets dropped.
- #424 (closed, 0.6.61): finalize fallback added for the gemma-4 streaming gap. The fallback ships but doesn't catch this case for Qwen3.6.
- #175 (closed): historical regression of `qwen3_xml` being aliased to `qwen3_coder_xml` in 0.6.6. Unrelated as far as I can tell — both parsers exhibit the same streaming drop on 0.6.61.

