"""Matrix for the hard12 workflow: one job per (task, arm)."""
import json
import os
import sys

SET = os.environ.get("TASKSET", "").strip()
if SET:  # data/sets/<SET>.txt: one task directory per line
    lines = [(None, line.strip()) for line in open(f"data/sets/{SET}.txt", encoding="utf-8") if line.strip()]
else:
    lines = [line.split() for line in open("data/night_tasks.txt", encoding="utf-8") if line.strip()]
want = [int(x) for x in os.environ.get("TASKS", "").split(",") if x.strip()]
arms = [a.strip() for a in os.environ.get("ARMS", "").split(",") if a.strip()]
# An arm may be a group run side by side in ONE job ("karox6+karox6b"; "trio" =
# karox6+opencode_v2+deepseek_harness): identical conditions, one runner IP.
# CHUNK > 1: one job runs that many tasks one after another (the runner, and so its IP,
# stays the same for hours: providers that limit IPs per key refuse fresh runners).
KNOWN = {"karox5", "karox6", "karox6b", "opencode_v2", "deepseek_harness", "codex", "claude_code", "oracle"}
GROUPS = {"trio": "karox6+opencode_v2+deepseek_harness", "trioc": "karox6+opencode_v2+claude_code"}
arms = [GROUPS.get(a, a) for a in arms]
bad = {p for a in arms for p in a.split("+")} - KNOWN
if bad or not arms:
    sys.exit(f"bad arms: {sorted(bad) or 'none'}")
chunk = max(int(os.environ.get("CHUNK", "1") or 1), 1)
# Dahl: keys are shared by every job, 3 parallel requests each. Pack the tasks into at
# most PARALLEL jobs per arm group, so all jobs run at once and job k can own key
# subset k (scripts/dahl_gateway.py): no two jobs ever send on the same key.
if os.environ.get("UPSTREAM") == "dahl2":
    lanes = max(int(os.environ.get("PARALLEL", "1") or 1), 1)
    n_tasks = len([1 for n, _ in enumerate(lines, 1) if not want or n in want])
    per_group = max(lanes // max(len(arms), 1), 1)
    chunk = max(chunk, -(-n_tasks // per_group))
picked = [(n, slug if SET else "hard12_tasks/h12-" + slug[:40])
          for n, (_key, slug) in enumerate(lines, 1) if not want or n in want]
include = []
for arm in arms:
    for i in range(0, len(picked), chunk):
        part = picked[i:i + chunk]
        include.append({
            "n": part[0][0] if chunk == 1 else f"c{i // chunk + 1:02d}",
            "nums": " ".join(str(n) for n, _ in part),
            "task": " ".join(t for _, t in part),
            "arm": arm,
            "armname": arm.replace("+", "-"),
            "slot": len(include),
        })
for job in include:
    job["slots"] = len(include)
print("matrix=" + json.dumps({"include": include}))
