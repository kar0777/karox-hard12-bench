"""Requests per task and arm from the gateway audit of downloaded runs (all rows and successes).

    python requests.py <run dir> [<run dir> ...]
"""
import collections
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
rows = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
status = collections.Counter()
seen = set()
first, last = None, None
for root in sys.argv[1:]:
    for path in glob.glob(os.path.join(root, "**", "*audit*.jsonl"), recursive=True):
        for line in open(path, encoding="utf-8"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            key = (e.get("run_id"), e.get("start_epoch"), e.get("ts"), e.get("input_tokens"),
                   e.get("output_tokens"), e.get("status"))
            if key in seen:
                continue
            seen.add(key)
            c = rows[str(e.get("task_id"))][str(e.get("harness"))]
            c["all"] += 1
            c["ok"] += e.get("status") == "success"
            status[(e.get("status"), str(e.get("error_class") or e.get("http_status") or ""))] += 1
            ts = e.get("start_epoch") or 0
            if ts:
                first = ts if first is None else min(first, ts)
                last = ts if last is None else max(last, ts)
total = collections.Counter()
for task in sorted(rows):
    parts = []
    for arm in sorted(rows[task]):
        c = rows[task][arm]
        parts.append(f"{arm} {c['all']} ({c['ok']} ok)")
        total[arm] += c["all"]
        total["all"] += c["all"]
    print(f"{task[:44]:44} " + "; ".join(parts) + f"  = {sum(rows[task][a]['all'] for a in rows[task])}")
print("total:", dict(total))
print("statuses:", dict(status))
if first:
    import datetime
    print("first", datetime.datetime.fromtimestamp(first, datetime.UTC).isoformat(),
          "last", datetime.datetime.fromtimestamp(last, datetime.UTC).isoformat())
