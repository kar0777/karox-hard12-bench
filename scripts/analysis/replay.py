"""Does each harness send reasoning back? Regress input growth on the previous call's reasoning tokens."""
import collections, glob, json, os, sys

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
                if k not in seen:
                    seen.add(k)
                    rows.append(e)
    return rows


def lstsq3(ps):
    # solve normal equations for d = a*r + b*v + c
    n = len(ps)
    S = [[0.0] * 3 for _ in range(3)]; T = [0.0] * 3
    for r, v, d in ps:
        x = (r, v, 1.0)
        for i in range(3):
            T[i] += x[i] * d
            for j in range(3):
                S[i][j] += x[i] * x[j]
    # gaussian elimination
    M = [S[i] + [T[i]] for i in range(3)]
    for i in range(3):
        p = max(range(i, 3), key=lambda k: abs(M[k][i]))
        M[i], M[p] = M[p], M[i]
        if abs(M[i][i]) < 1e-12:
            return (0.0, 0.0, 0.0)
        for k in range(3):
            if k != i:
                f = M[k][i] / M[i][i]
                M[k] = [a - f * b for a, b in zip(M[k], M[i])]
    return tuple(M[i][3] / M[i][i] for i in range(3))

for root in sys.argv[1:]:
    rows = [e for e in load(root) if e.get("status") == "success"]
    by = collections.defaultdict(list)
    for e in rows:
        by[(e.get("harness"), e.get("run_id"))].append(e)
    pts = collections.defaultdict(list)
    for (arm, _run), es in by.items():
        es.sort(key=lambda e: e.get("start_epoch") or 0)
        for a, b in zip(es, es[1:]):
            d = (b.get("input_tokens") or 0) - (a.get("input_tokens") or 0)
            r = a.get("reasoning_tokens") or 0
            v = (a.get("output_tokens") or 0) - r
            if 0 < d < 60000 and (b.get("sent") or {}).get("messages_count", 0) > (a.get("sent") or {}).get("messages_count", 0):
                pts[arm].append((r, v, d))
    print("==", root)
    for arm, ps in sorted(pts.items()):
        coef = lstsq3(ps)
        big = [(r, d) for r, v, d in ps if r > 3000]
        frac = sum(1 for r, d in big if d >= r * 0.8) / max(len(big), 1)
        print(f"  {arm:17} n={len(ps):5}  growth = {coef[0]:.2f}*reasoning + {coef[1]:.2f}*visible + {coef[2]:.0f};  steps with reasoning>3000: {len(big)}, of them growth>=0.8*reasoning: {frac:.0%}")
