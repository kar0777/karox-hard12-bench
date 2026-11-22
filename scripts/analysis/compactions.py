"""Compaction A/B: per KaroX trial, what each compaction did and what followed it.

    python compactions.py <run dir>
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for path in sorted(glob.glob(os.path.join(sys.argv[1], "**", "karox6.jsonl"), recursive=True)):
    trial_dir = os.path.dirname(os.path.dirname(path))
    result = json.load(open(os.path.join(trial_dir, "result.json"), encoding="utf-8"))
    arm = (result.get("agent_info") or {}).get("name")
    reward = ((result.get("verifier_result") or {}).get("rewards") or {}).get("reward")
    task = str(result.get("task_name", "?")).split("/")[-1]
    usage = []  # (step, input, cached)
    compactions = []  # (index into usage at that moment, event)
    fin = {}
    notices = []
    for line in open(path, encoding="utf-8"):
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t = e.get("type")
        if t == "usage":
            u = e["usage"]
            usage.append((e.get("step"), u.get("input_tokens") or 0, u.get("cached_tokens") or 0,
                          u.get("output_tokens") or 0))
        elif t == "compacted":
            compactions.append((len(usage), e))
        elif t == "run_finished":
            fin = e
        elif t == "notice":
            notices.append(e.get("kind"))
    peak = max((u[1] for u in usage), default=0)
    total_in = sum(u[1] for u in usage)
    total_cached = sum(u[2] for u in usage)
    total_out = sum(u[3] for u in usage)
    above = sum(u[1] for u in usage if u[1] > 170_000)
    print(f"== {task[:40]} {arm} reward={reward} status={fin.get('status')} reason={str(fin.get('reason'))[:40]} "
          f"steps={len(usage)} elapsed={fin.get('elapsed_s')}")
    print(f"   input {total_in / 1e6:.2f}M (cached {total_cached / max(total_in, 1):.0%}), uncached "
          f"{(total_in - total_cached) / 1e3:.0f}k, output {total_out / 1e3:.0f}k, peak context {peak / 1e3:.0f}k, "
          f"input spent above 170k: {above / 1e6:.2f}M ({above / max(total_in, 1):.0%}); notices {notices}")
    for index, e in compactions:
        nxt = usage[index] if index < len(usage) else None
        after = (f"next request: {nxt[1] / 1e3:.0f}k in, {nxt[2] / max(nxt[1], 1):.0%} cached"
                 if nxt else "no request after it")
        print(f"   compaction at call {index}: {e.get('mode')} {e.get('tokens_before', 0) / 1e3:.0f}k -> "
              f"{e.get('tokens_after', 0) / 1e3:.0f}k in {e.get('duration_s')} s; {after}")
