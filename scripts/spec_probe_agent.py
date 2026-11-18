"""Spec-reviewer probe, agent form: KaroX itself (same model, fresh session, read-only
tools) reviews a finished diff against the task statement and answers in its final reply.

python3 scripts/spec_probe_agent.py CASES_DIR OUT_DIR SAMPLES
The one-call form (spec_probe.py) lost every answer to the gateway's 32k output cap; in a
tool loop each step is short. Cases come from CASES_DIR/cases.json ("dir" names the probe
dir holding the inputs); the outcome is never shown. Key only from REFORMBOSS_API_KEY,
passed in the child's environment (karox reads and drops it), never in arguments or logs.
A run that started is never repeated.
"""

import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

BASE = "https://api.reformboss.com/v1"
MODEL = "deepseek-v4.1-flash-1017"

PROMPT = """You are reviewing a finished code change, not writing one. In the current \
directory, task.md is the task statement the change was meant to solve and change.diff is \
the final diff. The repository itself is not here. Do not create or modify files.

Read task.md fully, then change.diff (in parts if it is long). List each concrete \
requirement of the task statement that the diff does not implement, implements differently \
from what the statement says (names, signatures, return types and data shapes, formats, \
defaults, ordering, error types and messages, what must be preserved), or breaks. For each \
gap: quote the task sentence, name the file and code in the diff, and say exactly what \
differs. Report only gaps you can show from these two files: no style, docs or \
test-coverage remarks, and nothing that code outside the diff may already handle. Tests \
the author added prove only what the author believed.

Your final reply is the review. If there are no such gaps, the final reply is exactly: \
NO GAPS"""


def run_one(cases_root, out_dir, entry, k, key):
    case = entry["case"]
    src = os.path.join(cases_root, entry.get("dir", ""), case)
    work = tempfile.mkdtemp(prefix="review-")
    home = tempfile.mkdtemp(prefix="karoxhome-")
    shutil.copy(os.path.join(src, "instruction.md"), os.path.join(work, "task.md"))
    shutil.copy(os.path.join(src, "agent.diff"), os.path.join(work, "change.diff"))
    cmd = [
        sys.executable, "-m", "karox6", "run", "--json",
        "--provider", "openai-chat", "--base-url", BASE,
        "--api-key-env", "REFORMBOSS_API_KEY", "--model", MODEL,
        "--home", home, "--cwd", work, "--approve-dangerous", "deny",
        "--max-seconds", "1200", "--max-steps", "60", "--no-mcp",
        "--", PROMPT,
    ]
    env = {**os.environ, "REFORMBOSS_API_KEY": key}
    started = time.time()
    proc = subprocess.run(
        cmd, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=1500, check=False,
    )
    rec = {"case": case, "sample": k, "seconds": round(time.time() - started, 1),
           "exit": proc.returncode}
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "run_finished":
            rec.update(
                content=event.get("final_text") or "",
                status=event.get("status"),
                reason=event.get("reason"),
                steps=event.get("steps"),
                usage=event.get("usage"),
            )
    if "content" not in rec:
        rec["stderr_tail"] = proc.stderr[-1500:]
    changed = sorted(set(os.listdir(work)) - {"task.md", "change.diff"})
    rec["extra_files"] = changed
    with open(os.path.join(out_dir, f"{case}.{k}.json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
    print(case, k, rec["seconds"], rec.get("status"), rec.get("steps"), flush=True)
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(home, ignore_errors=True)


def main():
    cases_dir, out_dir, samples = sys.argv[1], sys.argv[2], int(sys.argv[3])
    key = os.environ.pop("REFORMBOSS_API_KEY", "")
    if not key:
        sys.exit("no REFORMBOSS_API_KEY")
    os.makedirs(out_dir, exist_ok=True)
    cases = json.load(open(os.path.join(cases_dir, "cases.json"), encoding="utf-8"))
    root = os.path.dirname(os.path.abspath(cases_dir))
    jobs = [(c, k) for c in cases for k in range(samples)]
    for c in cases:
        c.setdefault("dir", os.path.basename(os.path.abspath(cases_dir)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get("PROBE_WORKERS", "2"))) as pool:
        list(pool.map(lambda j: run_one(root, out_dir, j[0], j[1], key), jobs))


if __name__ == "__main__":
    main()
