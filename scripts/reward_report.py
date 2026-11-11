"""Official-reward report for external task sets: solved = reward.txt == 1.

    python3 reward_report.py <jobs_dir> [<audit.jsonl>]
"""
import collections
import datetime as dt
import glob
import json
import sys

jobs = sys.argv[1]
rows = collections.defaultdict(list)
cells = collections.defaultdict(dict)
for f in glob.glob(f"{jobs}/*/*__*/result.json"):
    r = json.load(open(f, encoding="utf-8"))
    arm = ((r.get("agent_info") or {}).get("model_info") or {}).get("name") or "?"
    arm = arm.split("/")[-1].removeprefix("hard12-")
    reward = ((r.get("verifier_result") or {}).get("rewards") or {}).get("reward")
    exc = (r.get("exception_info") or {}).get("exception_type")
    ex = r.get("agent_execution") or {}
    try:
        mins = (dt.datetime.fromisoformat(ex["finished_at"].replace("Z", "+00:00"))
                - dt.datetime.fromisoformat(ex["started_at"].replace("Z", "+00:00"))).total_seconds() / 60
    except Exception:  # noqa: BLE001
        mins = None
    task = r.get("task_name", "?").split("/")[-1]
    ok = reward == 1.0
    rows[arm].append((ok, mins, exc))
    cells[task].setdefault(arm, []).append("1" if ok else ("E" if exc and reward is None else "0"))
arms = sorted(rows)
print("| task | " + " | ".join(arms) + " |\n|---|" + "---|" * len(arms))
for task in sorted(cells):
    print(f"| {task} | " + " | ".join("".join(cells[task].get(a, [])) or "-" for a in arms) + " |")
print("\n| arm | trials | solved | rate | errors | agent min/trial |\n|---|---|---|---|---|---|")
for a in arms:
    v = rows[a]
    m = [x[1] for x in v if x[1] is not None]
    print(f"| {a} | {len(v)} | {sum(x[0] for x in v)} | {sum(x[0] for x in v) / len(v):.0%} | "
          f"{sum(1 for x in v if x[2] and not x[0])} | {sum(m) / max(len(m), 1):.1f} |")
