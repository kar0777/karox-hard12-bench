"""Simulate a lower compaction threshold on recorded karox6 runs (gateway audit input tokens).
Cost unit: cached-equivalent tokens (uncached = 10x)."""
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

def sim(ins, T, R):
    """ins: recorded per-call input tokens (no compaction assumed below 300k). Returns (sum_inputs, n_compactions, extra_cost)."""
    removed = 0; total = 0; n = 0; extra = 0
    for x in ins:
        cur = x - removed
        if cur > T:
            # summary call on the cached prefix, then restart at R (uncached once)
            extra += cur * 1 + R * 9
            removed += cur - R
            cur = R
            n += 1
        total += cur
    return total, n, extra

for root in sys.argv[1:]:
    rows = [e for e in load(root) if e.get("status") == "success" and e.get("harness") == "karox6"]
    by = collections.defaultdict(list)
    for e in rows:
        by[e.get("run_id")].append(e)
    base = 0; res = collections.defaultdict(lambda: [0, 0, 0])
    for run, es in by.items():
        es.sort(key=lambda e: e.get("start_epoch") or 0)
        ins = [e.get("input_tokens") or 0 for e in es]
        if max(ins) > 300_000:
            continue  # already compacted at 320k in the recording: skip (trajectory not monotone)
        base += sum(ins)
        for T in (120_000, 150_000, 170_000, 200_000):
            t, n, x = sim(ins, T, 45_000)
            res[T][0] += t; res[T][1] += n; res[T][2] += x
    print(f"== {os.path.basename(root)}: karox6 runs {len(by)}, input {base/1e6:.1f}M (cached-equivalent)")
    for T, (t, n, x) in sorted(res.items()):
        print(f"   compact at {T//1000}k: input {t/1e6:6.1f}M + compaction overhead {x/1e6:5.1f}M = {(t+x)/1e6:6.1f}M ({(t+x)/base-1:+.0%}), compactions {n}")
