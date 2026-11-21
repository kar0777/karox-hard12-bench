import collections, glob, json, os, sys
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
root = sys.argv[1]
rows = [e for e in load(root) if e.get("status") == "success"]
by = collections.defaultdict(list)
for e in rows:
    by[(e.get("task_id"), e.get("harness"))].append(e)
for (task, arm), es in sorted(by.items()):
    es.sort(key=lambda e: e.get("start_epoch") or 0)
    ins = [e.get("input_tokens") or 0 for e in es]
    drops = [(i, a, b) for i, (a, b) in enumerate(zip(ins, ins[1:])) if b < a * 0.7 and a > 20000]
    peak = max(ins)
    print(f"{task[:30]:30} {arm[:10]:10} calls {len(ins):4} peak {peak/1000:6.0f}k last {ins[-1]/1000:6.0f}k mean {sum(ins)/len(ins)/1000:6.0f}k  drops>30%: {[(i, round(a/1000), round(b/1000)) for i, a, b in drops][:6]}")
