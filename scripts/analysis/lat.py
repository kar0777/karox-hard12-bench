import collections, glob, json, os, sys
def load(root):
    rows, seen = [], set()
    for path in glob.glob(os.path.join(root, "**", "*audit*.jsonl"), recursive=True):
        for line in open(path, encoding="utf-8"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            k = (e.get("run_id"), e.get("start_epoch"), e.get("ts"), e.get("input_tokens"), e.get("output_tokens"))
            if k not in seen:
                seen.add(k); rows.append(e)
    return rows
for root in sys.argv[1:]:
    rows = load(root)
    print("==", os.path.basename(root), len(rows))
    by = collections.defaultdict(list)
    for e in rows:
        by[e.get("harness")].append(e)
    for arm, es in sorted(by.items()):
        ok = [e for e in es if e.get("status") == "success"]
        bad = [e for e in es if e.get("status") != "success"]
        lat = sorted(e.get("latency_s") or 0 for e in ok)
        if not lat:
            continue
        slow = [e for e in ok if (e.get("latency_s") or 0) > 300]
        tps = [((e.get("output_tokens") or 0) / max((e.get("latency_s") or 0) - (e.get("ttft_s") or 0), 0.5)) for e in ok if (e.get("output_tokens") or 0) > 500]
        tps.sort()
        kinds = collections.Counter((str(e.get("status")), str(e.get("error_class") or e.get("error_type") or e.get("exception") or "")[:60]) for e in bad)
        print(f"  {arm:17} ok {len(ok):5} failed {len(bad):4}  latency p50 {lat[len(lat)//2]:6.1f} p90 {lat[int(len(lat)*.9)]:6.1f} p99 {lat[int(len(lat)*.99)]:6.1f} max {lat[-1]:6.1f}  >300s: {len(slow)} (sum {sum(e['latency_s'] for e in slow)/60:.0f} min)  tok/s p50 {tps[len(tps)//2] if tps else 0:.0f}")
        if bad:
            print("       failures:", dict(kinds.most_common(4)), "keys:", sorted(set(bad[0].keys()) - set(ok[0].keys()))[:8])
