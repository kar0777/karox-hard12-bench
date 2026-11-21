import collections, glob, json, os, statistics, sys
def load(root):
    rows, seen = [], set()
    for path in glob.glob(os.path.join(root, "**", "*audit*.jsonl"), recursive=True):
        for line in open(path, encoding="utf-8"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            k = (e.get("run_id"), e.get("start_epoch"), e.get("ts"), e.get("input_tokens"))
            if k not in seen:
                seen.add(k); rows.append(e)
    return rows
B = ((25_000, "<25k"), (50_000, "25-50k"), (100_000, "50-100k"), (170_000, "100-170k"), (10**9, ">170k"))
for root in sys.argv[1:]:
    rows = [e for e in load(root) if e.get("status") == "success"]
    by = collections.defaultdict(lambda: collections.defaultdict(list))
    for e in rows:
        x = e.get("input_tokens") or 0
        b = next(name for lim, name in B if x < lim)
        by[e.get("harness")][b].append((e.get("reasoning_tokens") or 0, (e.get("output_tokens") or 0) - (e.get("reasoning_tokens") or 0), e.get("latency_s") or 0, e.get("ttft_s") or 0))
    print("==", os.path.basename(root))
    for arm in sorted(by):
        cells = []
        for _, name in B:
            v = by[arm].get(name)
            if v:
                cells.append(f"{name}: n{len(v):4} r {statistics.mean(x[0] for x in v):5.0f} lat {statistics.mean(x[2] for x in v):5.1f}s ttft {statistics.mean(x[3] for x in v):4.1f}")
        print(f"  {arm[:10]:10} " + " | ".join(cells))
