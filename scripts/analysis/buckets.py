import collections, glob, json, os, statistics, sys
sys.path.insert(0, ".")
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stepcmp.py"), encoding="utf-8").read().split("root = sys.argv[1]")[0])

def bucket(n):
    for lim, name in ((150, "<150"), (400, "150-400"), (1000, "400-1k"), (3000, "1k-3k")):
        if n < lim:
            return name
    return ">3k"

def table(label, steps):
    print(label)
    for c in ("shell", "edit", "look"):
        rows = collections.defaultdict(list)
        for s in steps:
            if s["cat"] == c:
                rows[bucket(s["argchars"])].append(s["rchars"])
        n = sum(len(v) for v in rows.values())
        for b in ("<150", "150-400", "400-1k", "1k-3k", ">3k"):
            v = rows.get(b)
            if v:
                print(f"   {c:6} args {b:8} steps {len(v):5} ({len(v)/n:4.0%})  reasoning mean {statistics.mean(v):7.0f} median {statistics.median(v):6.0f}")

for root in sys.argv[1:]:
    k, o = [], []
    for path in glob.glob(os.path.join(root, "**", "session.jsonl"), recursive=True):
        if ".review" in path or ".agent-" in path:
            continue
        k += karox_steps(path)
    for path in glob.glob(os.path.join(root, "**", "opencode.txt"), recursive=True):
        o += opencode_steps(path)
    print("=====", os.path.basename(root))
    if k: table("karox6", k)
    if o: table("opencode_v2", o)
