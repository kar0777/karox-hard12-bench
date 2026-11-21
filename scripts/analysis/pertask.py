import collections, glob, json, os, statistics, sys

def load(root):
    rows, seen = [], set()
    for path in glob.glob(os.path.join(root, "**", "*audit*.jsonl"), recursive=True):
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                k = (e.get("run_id"), e.get("start_epoch"), e.get("ts"), e.get("input_tokens"), e.get("output_tokens"))
                if k in seen:
                    continue
                seen.add(k)
                rows.append(e)
    return rows

root = sys.argv[1]
rows = [e for e in load(root) if e.get("status") == "success"]
by = collections.defaultdict(lambda: collections.defaultdict(list))
for e in rows:
    by[e.get("task_id")][e.get("harness")].append(e)
arms = sorted({e.get("harness") for e in rows})
print("task".ljust(34), *(f"{a[:8]:>30}" for a in arms))
first = collections.defaultdict(list)
for task in sorted(by):
    cells = []
    for a in arms:
        es = sorted(by[task].get(a, []), key=lambda e: e.get("start_epoch") or 0)
        if not es:
            cells.append(" " * 30)
            continue
        n = len(es)
        rs = sum(e.get("reasoning_tokens") or 0 for e in es)
        out = sum(e.get("output_tokens") or 0 for e in es)
        r1 = es[0].get("reasoning_tokens") or 0
        first[a].append(r1)
        cells.append(f"n{n:4} r/c{rs/n:6.0f} v/c{(out-rs)/n:5.0f} r1 {r1:5}")
    print(task[:34].ljust(34), *cells)
print()
for a in arms:
    if first[a]:
        print(a, "first-call reasoning: mean", round(statistics.mean(first[a])), "median", statistics.median(first[a]))
