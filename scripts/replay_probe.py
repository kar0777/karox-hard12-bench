"""Counterfactual replay probe: send a saved agent request (cut from a real trajectory,
possibly with an injected variant message) and record what the model does next.

python3 scripts/replay_probe.py CASES_DIR OUT_DIR SAMPLES
Reads CASES_DIR/cases.json and CASES_DIR/<case>/request.json.gz (an OpenAI chat body). The
frozen sampling profile is enforced (same as the hard12 gateway). Key only from
REFORMBOSS_API_KEY; it is never printed. A request that was sent and failed is not
retried (a paid call may have run); only 429 refusals are retried. Output per sample:
tool call names, text, finish_reason, usage, seconds.
"""

import concurrent.futures
import gzip
import json
import os
import sys
import time
import urllib.error
import urllib.request

# Upstream per probe dir: a file <cases>/.upstream holding "dahl" picks the GLM-5.3-Flash dev
# lane (key DAHL_API_KEY); otherwise the bench model on ReformBoss.
UPSTREAMS = {
    "reformboss": ("https://api.reformboss.com/v1/chat/completions",
                   "deepseek-v4.1-flash-1017", "REFORMBOSS_API_KEY"),
    "dahl": ("https://inference.dahl.global/v1/chat/completions",
             "zai-org/GLM-5.3-Flash", "DAHL_API_KEY"),
    "dahl2": ("https://inference.dahl.global/v1/chat/completions",
              "zai-org/GLM-5.3-Flash", "DAHL_API_KEY_2"),
}
BASE, MODEL, KEYVAR = UPSTREAMS["reformboss"]
EFFORT = "max"
STATS = {"429": 0}


def call(key, body):
    data = json.dumps(body).encode()
    for attempt in range(8):
        req = urllib.request.Request(
            BASE, data=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        )
        started = time.time()
        try:
            with urllib.request.urlopen(req, timeout=900) as resp:
                return json.loads(resp.read()), round(time.time() - started, 1), None
        except urllib.error.HTTPError as exc:
            # 429, or 503 "at capacity": refused before any work, so a retry is safe
            if exc.code in (429, 503) and attempt < 7:
                STATS["429"] += 1
                time.sleep(3 + attempt * 4)
                continue
            text = exc.read()[:300].decode("utf-8", "replace") if exc.fp else ""
            return None, round(time.time() - started, 1), f"HTTP {exc.code} {text}"
        except Exception as exc:  # sent and failed: do not repeat a possibly paid call
            return None, round(time.time() - started, 1), f"{type(exc).__name__}: {exc}"[:300]
    return None, 0, "429 exhausted"


def main():
    cases_dir, out_dir, samples = sys.argv[1], sys.argv[2], int(sys.argv[3])
    global BASE, MODEL, KEYVAR, EFFORT
    marker = os.path.join(cases_dir, ".upstream")
    if os.path.exists(marker):
        BASE, MODEL, KEYVAR = UPSTREAMS[open(marker, encoding="utf-8").read().strip()]
    # <cases>/.effort overrides the profile's reasoning effort (a reviewer call, not an
    # agent step: "max" can spend the whole output on reasoning)
    effort_file = os.path.join(cases_dir, ".effort")
    if os.path.exists(effort_file):
        EFFORT = open(effort_file, encoding="utf-8").read().strip()
    key = os.environ.get(KEYVAR, "")
    if not key:
        sys.exit(f"no {KEYVAR}")
    os.makedirs(out_dir, exist_ok=True)
    cases = json.load(open(os.path.join(cases_dir, "cases.json"), encoding="utf-8"))
    # sample-major order: every case gets its first sample before any gets a second
    jobs = [(c["case"], k) for k in range(samples) for c in cases]

    def run(job):
        case, k = job
        path = os.path.join(out_dir, f"{case}.{k}.json")
        if os.path.exists(path):
            return
        with gzip.open(os.path.join(cases_dir, case, "request.json.gz"), "rt", encoding="utf-8") as f:
            body = json.load(f)
        body.update(model=MODEL, temperature=1.0, top_p=0.95, max_tokens=32768,
                    reasoning_effort=EFFORT, stream=False)
        body.pop("stream_options", None)
        out, secs, err = call(key, body)
        rec = {"case": case, "sample": k, "seconds": secs, "error": err}
        if out:
            msg = out["choices"][0]["message"]
            rec["tool_calls"] = [c["function"]["name"] for c in msg.get("tool_calls") or []]
            rec["tool_args"] = [c["function"]["arguments"][:400] for c in msg.get("tool_calls") or []]
            rec["content"] = (msg.get("content") or "")[:3000]
            rec["finish_reason"] = out["choices"][0].get("finish_reason")
            rec["usage"] = out.get("usage")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=1)
        print(case, k, secs, err or (rec.get("tool_calls") or "STOP"), flush=True)

    workers = int(os.environ.get("PROBE_WORKERS", "2"))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(run, jobs))
    print("workers", workers, "429 refusals", STATS["429"], flush=True)


if __name__ == "__main__":
    main()
