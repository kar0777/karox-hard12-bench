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
for root in sys.argv[1:]:
    rows = [e for e in load(root) if e.get("status") == "success"]
    by = collections.defaultdict(list)
    for e in rows:
        by[(e.get("harness"), e.get("run_id"))].append(e.get("input_tokens") or 0)
    print("==", os.path.basename(root))
    arms = collections.defaultdict(list)
    for (arm, _), ins in by.items():
        arms[arm].append(ins)
    for arm, runs in sorted(arms.items()):
        tot = sum(sum(r) for r in runs)
        for lim in (100_000, 150_000, 200_000):
            over_runs = sum(1 for r in runs if max(r) > lim)
            over_tok = sum(x for r in runs for x in r if x > lim)
            excess = sum(x - lim for r in runs for x in r if x > lim)
            print(f"  {arm:17} runs {len(runs):3}  peak>{lim//1000}k: {over_runs:3} runs; tokens in calls above it {over_tok/tot:5.1%} of input; excess over the line {excess/tot:5.1%}")
