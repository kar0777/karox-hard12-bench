"""Spec-reviewer probe: does an independent reviewer (same model, fresh context, only the
task statement and the final diff) name the requirement a failed trial missed, and how
often does it raise a gap on trials that passed?

python3 scripts/spec_probe.py CASES_DIR OUT_DIR SAMPLES
Reads CASES_DIR/<case>/{instruction.md,agent.diff}; the outcome in cases.json is never
sent. Key only from REFORMBOSS_API_KEY; it is never printed. A request that was sent and
failed is not retried (a paid call may have run); only 429 refusals are retried.
"""

import concurrent.futures
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://api.reformboss.com/v1/chat/completions"
MODEL = "deepseek-v4.1-flash-1017"
MAX_DIFF_CHARS = 240_000

SYSTEM = (
    "You review a finished code change against the task it was meant to solve. You see "
    "only the task statement and the final diff, not the author's reasoning or test runs."
)
USER = """TASK STATEMENT:
<task>
{task}
</task>

FINAL DIFF:
<diff>
{diff}
</diff>

List each concrete requirement of the task statement that this diff does not implement,
implements differently from what the statement says (names, signatures, return types and
data shapes, formats, defaults, ordering, error types and messages, what must be
preserved), or breaks. For each gap: quote the task sentence, name the file and code in
the diff, and say exactly what differs. Report only gaps you can show from these two
texts: no style, docs or test-coverage remarks, and nothing that code outside the diff
may already handle. Tests the author added prove only what the author believed.
If there are no such gaps, answer exactly: NO GAPS"""


def call(key, task, diff):
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": USER.format(task=task, diff=diff)},
        ],
        "temperature": 1.0,
        "top_p": 0.95,
        "max_tokens": 32768,
        "reasoning_effort": "max",
        "stream": False,
    }
    data = json.dumps(body).encode()
    for attempt in range(6):
        req = urllib.request.Request(
            BASE,
            data=data,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        )
        started = time.time()
        try:
            with urllib.request.urlopen(req, timeout=900) as resp:
                out = json.loads(resp.read())
            return out, round(time.time() - started, 1), None
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 5:
                time.sleep(2 + attempt * 3)
                continue
            body = exc.read()[:300].decode("utf-8", "replace") if exc.fp else ""
            return None, round(time.time() - started, 1), f"HTTP {exc.code} {body}"
        except Exception as exc:  # sent and failed: do not repeat a possibly paid call
            return None, round(time.time() - started, 1), f"{type(exc).__name__}: {exc}"[:300]
    return None, 0, "429 exhausted"


def main():
    cases_dir, out_dir, samples = sys.argv[1], sys.argv[2], int(sys.argv[3])
    key = os.environ.get("REFORMBOSS_API_KEY", "")
    if not key:
        sys.exit("no REFORMBOSS_API_KEY")
    os.makedirs(out_dir, exist_ok=True)
    cases = json.load(open(os.path.join(cases_dir, "cases.json"), encoding="utf-8"))
    # Optional prompt override (prompt.json: {"system": ..., "user": ...}); cases.json may
    # list cases kept in another probe dir ("dir" key) so variants reuse the same inputs.
    global SYSTEM, USER
    override = os.path.join(cases_dir, "prompt.json")
    if os.path.exists(override):
        prompt = json.load(open(override, encoding="utf-8"))
        SYSTEM, USER = prompt["system"], prompt["user"]
    jobs = [(c["case"], k) for c in cases for k in range(samples)]

    def run(job):
        case, k = job
        entry = next(c for c in cases if c["case"] == case)
        base = os.path.join(os.path.dirname(cases_dir.rstrip("/")), entry.get("dir", ""), case)
        if not entry.get("dir"):
            base = os.path.join(cases_dir, case)
        task = open(os.path.join(base, "instruction.md"), encoding="utf-8").read()
        diff = open(os.path.join(base, "agent.diff"), encoding="utf-8").read()
        if len(diff) > MAX_DIFF_CHARS:
            diff = diff[:MAX_DIFF_CHARS] + "\n... (diff truncated)"
        out, secs, err = call(key, task, diff)
        rec = {"case": case, "sample": k, "seconds": secs, "error": err}
        if out:
            msg = out["choices"][0]["message"]
            rec["content"] = msg.get("content") or ""
            rec["reasoning_chars"] = len(msg.get("reasoning_content") or "")
            rec["finish_reason"] = out["choices"][0].get("finish_reason")
            rec["usage"] = out.get("usage")
        with open(os.path.join(out_dir, f"{case}.{k}.json"), "w", encoding="utf-8") as f:
            json.dump(rec, f, ensure_ascii=False, indent=1)
        print(case, k, secs, err or rec.get("finish_reason"), flush=True)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(run, jobs))


if __name__ == "__main__":
    main()
