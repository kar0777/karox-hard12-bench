"""A chat-completions upstream that logs every request body and answers with scripted turns.

usage: mock_chat.py LOG.jsonl PORT [strict]

Turn 1: one tool call (the first function tool the request offers, or plain text when it
offers none); later turns: the text "done". With `strict`, a request is refused with 400
the way a strict chat-completions upstream would: a `developer` role, a tool that is not a
function, or a field outside a small accepted set.
"""
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG, PORT = sys.argv[1], int(sys.argv[2])
STRICT = len(sys.argv) > 3 and sys.argv[3] == "strict"
ACCEPTED = {"model", "messages", "tools", "tool_choice", "temperature", "top_p", "max_tokens",
            "stream", "stream_options", "reasoning_effort", "stop"}
LOCK = threading.Lock()
STATE = {"n": 0}


def chunk(delta, finish=None, usage=None):
    body = {"id": "mock", "object": "chat.completion.chunk", "created": int(time.time()),
            "model": "mock", "choices": [{"index": 0, "delta": delta, "finish_reason": finish}]}
    if usage is not None:
        body["usage"] = usage
    return b"data: " + json.dumps(body).encode() + b"\n\n"


def refusal(request):
    if not STRICT:
        return None
    extra = sorted(set(request) - ACCEPTED)
    if extra:
        return f"unknown fields: {extra}"
    roles = {m.get("role") for m in request.get("messages") or []}
    if roles - {"system", "user", "assistant", "tool"}:
        return f"unknown roles: {sorted(roles - {'system', 'user', 'assistant', 'tool'})}"
    bad = [t.get("type") for t in request.get("tools") or [] if t.get("type") != "function"]
    if bad:
        return f"unsupported tool types: {bad}"
    return None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        body = json.dumps({"object": "list", "data": [{"id": "mock", "object": "model"}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        why = refusal(request)
        with LOCK:
            STATE["n"] += 1
            n = STATE["n"]
            with open(LOG, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"n": n, "path": self.path, "refused": why, "body": request}) + "\n")
        if why:
            body = json.dumps({"error": {"message": why, "type": "invalid_request_error",
                                         "code": "invalid_parameter_error"}}).encode()
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        tools = [t for t in request.get("tools") or [] if t.get("type") == "function"]
        asked = any(m.get("role") == "tool" for m in request.get("messages") or [])
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        usage = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        if tools and not asked:
            name = tools[0]["function"]["name"]
            args = json.dumps({"command": ["bash", "-lc", "echo hello"]} if "shell" in name else {})
            call = {"index": 0, "id": "call_1", "type": "function",
                    "function": {"name": name, "arguments": args}}
            self.wfile.write(chunk({"role": "assistant", "tool_calls": [call]}))
            self.wfile.write(chunk({}, "tool_calls", usage))
        else:
            self.wfile.write(chunk({"role": "assistant", "content": "done"}))
            self.wfile.write(chunk({}, "stop", usage))
        self.wfile.write(b"data: [DONE]\n\n")
        self.wfile.flush()


ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
