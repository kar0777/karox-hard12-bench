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
bad = set(arms) - {"karox5", "opencode_v2", "deepseek_harness"}
if bad or not arms:
    sys.exit(f"bad arms: {sorted(bad) or 'none'}")
include = [
    {"n": n, "task": slug if SET else "hard12_tasks/h12-" + slug[:40], "arm": arm}
    for n, (_key, slug) in enumerate(lines, 1)
    if not want or n in want
    for arm in arms
]
print("matrix=" + json.dumps({"include": include}))
