"""Tool errors and waits in karox6 event logs (karox6.jsonl) of run dirs."""
import collections, glob, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
errs = collections.Counter(); samples = collections.defaultdict(list)
dur = collections.defaultdict(list); n_calls = collections.Counter(); runs = 0
for root in sys.argv[1:]:
    for path in glob.glob(os.path.join(root, "**", "karox6.jsonl"), recursive=True):
        runs += 1
        started = {}
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            t = e.get("type")
            if t == "tool_started":
                started[e["call_id"]] = e
            elif t == "tool_finished":
                name = e["name"]
                if "/" in name:
                    continue
                n_calls[name] += 1
                dur[name].append(e.get("duration_ms", 0) / 1000)
                out = e.get("output") or ""
                meta = e.get("meta") or {}
                if e.get("is_error"):
                    first = out.strip().splitlines()[0][:110] if out.strip() else ""
                    key = re.sub(r"[0-9]+", "N", first)
                    key = re.sub(r"'[^']*'|\"[^\"]*\"|/[\w./-]+", "X", key)[:70]
                    errs[(name, key)] += 1
                    if len(samples[(name, key)]) < 2:
                        samples[(name, key)].append(first)
                if meta.get("timed_out"):
                    errs[(name, "TIMED OUT -> job")] += 1
                if "truncated" in out[-400:].lower() or meta.get("spill_path"):
                    errs[(name, "output truncated/spilled")] += 1
print("runs", runs, "calls", dict(n_calls))
for (name, key), n in errs.most_common(40):
    print(f"{n:5}  {name:10} {key}   e.g. {samples[(name, key)][:1]}")
print()
for name, ds in sorted(dur.items(), key=lambda kv: -sum(kv[1])):
    ds2 = sorted(ds)
    print(f"{name:11} n={len(ds):5} total {sum(ds)/60:7.1f} min  mean {sum(ds)/len(ds):6.1f}s  p50 {ds2[len(ds2)//2]:6.1f}  p90 {ds2[int(len(ds2)*0.9)]:6.1f}  p99 {ds2[int(len(ds2)*0.99)]:6.1f} max {ds2[-1]:6.1f}  >60s: {sum(1 for d in ds if d>60)}  >290s: {sum(1 for d in ds if d>290)}")
