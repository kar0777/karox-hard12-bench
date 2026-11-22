"""Where in a run the output tokens go, per arm (gateway audit): thirds of each run's calls.

    python thirds.py <run dir> [<run dir> ...]

Each trial's successful calls are put in order and cut into three equal parts; reasoning
and visible output (text and tool-call arguments), calls and model time are summed per
part over all trials of an arm.
"""
import collections
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
calls = collections.defaultdict(list)
seen = set()
for root in sys.argv[1:]:
    for path in glob.glob(os.path.join(root, "**", "*audit*.jsonl"), recursive=True):
        for line in open(path, encoding="utf-8"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if e.get("status") != "success":
                continue
            key = (e.get("run_id"), e.get("start_epoch"), e.get("input_tokens"), e.get("output_tokens"))
            if key in seen:
                continue
            seen.add(key)
            calls[(str(e.get("task_id")), str(e.get("harness")))].append(e)
total = collections.defaultdict(collections.Counter)
for (_task, arm), rows in calls.items():
    rows.sort(key=lambda e: e.get("start_epoch") or 0)
    for i, e in enumerate(rows):
        third = min(i * 3 // len(rows), 2)
        c = total[arm]
        reasoning = e.get("reasoning_tokens") or 0
        c[f"reasoning{third}"] += reasoning
        c[f"visible{third}"] += (e.get("output_tokens") or 0) - reasoning
        c[f"calls{third}"] += 1
        c[f"seconds{third}"] += e.get("latency_s") or 0
for arm, c in sorted(total.items()):
    print(
        f"{arm:17} reasoning k {[round(c[f'reasoning{i}'] / 1000, 1) for i in range(3)]} "
        f"visible k {[round(c[f'visible{i}'] / 1000, 1) for i in range(3)]} "
        f"calls {[c[f'calls{i}'] for i in range(3)]} "
        f"model min {[round(c[f'seconds{i}'] / 60, 1) for i in range(3)]}"
    )
