import collections, glob, json, os, statistics, sys

def load(root):
    rows = []
    for path in glob.glob(os.path.join(root, "**", "*audit*.jsonl"), recursive=True):
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                rows.append(e)
    # dedupe (all_audit + per-trial copies)
    seen, out = set(), []
    for e in rows:
        k = (e.get("run_id"), e.get("start_epoch"), e.get("ts"), e.get("input_tokens"), e.get("output_tokens"))
        if k in seen:
            continue
        seen.add(k)
        out.append(e)
    return out

for root in sys.argv[1:]:
    rows = load(root)
    by = collections.defaultdict(list)
    for e in rows:
        if e.get("status") == "success":
            by[e.get("harness")].append(e)
    print(f"== {root}: {len(rows)} audit rows")
    for arm, es in sorted(by.items()):
        n = len(es)
        inp = sum(e.get("input_tokens") or 0 for e in es)
        cached = sum(e.get("cached_input_tokens") or 0 for e in es)
        out = sum(e.get("output_tokens") or 0 for e in es)
        rs = sum(e.get("reasoning_tokens") or 0 for e in es)
        lat = sum(e.get("latency_s") or 0 for e in es)
        med_r = statistics.median([e.get("reasoning_tokens") or 0 for e in es])
        med_o = statistics.median([e.get("output_tokens") or 0 for e in es])
        ttft = statistics.median([e.get("ttft_s") or 0 for e in es if e.get("ttft_s")]) if any(e.get("ttft_s") for e in es) else 0
        print(f"  {arm:17} calls {n:5}  in/call {inp/n:8.0f} (cached {cached/max(inp,1):.0%})  out/call {out/n:6.0f} (median {med_o:.0f})  reasoning/call {rs/n:6.0f} (median {med_r:.0f})  visible/call {(out-rs)/n:5.0f}  lat/call {lat/n:5.1f}s ttft {ttft:.1f}s")
