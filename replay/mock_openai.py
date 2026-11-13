"""A scripted OpenAI-compatible Chat Completions endpoint for offline replay.

No model is called. Each POST to /v1/chat/completions returns the next turn of
a scenario as a streamed tool call (SSE, the shape KaroX's provider expects),
and every request is logged so a checker can assert what KaroX sent back after
each tool ran. When the script is exhausted it keeps answering with finish.

usage: mock_openai.py SCENARIO.json LOG.jsonl PORT
"""

from __future__ import annotations

import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SCENARIO = json.load(open(sys.argv[1], encoding="utf-8"))
LOG = sys.argv[2]
PORT = int(sys.argv[3])
TURNS = SCENARIO["turns"]
FINISH = {"name": "finish", "arguments": {"answer": SCENARIO.get("answer", "done")}}
LOCK = threading.Lock()
STATE = {"index": 0}


def _chunk(delta: dict, finish: str | None = None, usage: dict | None = None) -> bytes:
    body = {"id": "replay", "object": "chat.completion.chunk", "created": int(time.time()),
            "model": "replay", "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]}
    if usage is not None:
        body["usage"] = usage
    return b"data: " + json.dumps(body).encode() + b"\n\n"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # quiet
        pass

    def do_GET(self):
        body = json.dumps({"object": "list", "data": [{"id": "replay", "object": "model"}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        request = json.loads(self.rfile.read(length) or b"{}")
        with LOCK:
            index = STATE["index"]
            STATE["index"] += 1
            turn = TURNS[index] if index < len(TURNS) else {"tool_calls": [FINISH]}
            with open(LOG, "a", encoding="utf-8") as handle:
                handle.write(json.dumps({
                    "index": index,
                    "at": time.time(),
                    "tools": sorted(t.get("function", {}).get("name", "") for t in request.get("tools") or []),
                    "messages": [
                        {"role": m.get("role"), "content": m.get("content") if isinstance(m.get("content"), str)
                         else json.dumps(m.get("content"))}
                        for m in request.get("messages") or []
                    ],
                }) + "\n")
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        out = [_chunk({"role": "assistant", "content": turn.get("content", f"step {index}")})]
        for position, call in enumerate(turn.get("tool_calls") or []):
            out.append(_chunk({"tool_calls": [{
                "index": position, "id": f"call_{index}_{position}", "type": "function",
                "function": {"name": call["name"], "arguments": json.dumps(call.get("arguments") or {})},
            }]}))
        out.append(_chunk({}, finish="tool_calls" if turn.get("tool_calls") else "stop",
                          usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}))
        out.append(b"data: [DONE]\n\n")
        for piece in out:
            self.wfile.write(piece)
        self.wfile.flush()


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
