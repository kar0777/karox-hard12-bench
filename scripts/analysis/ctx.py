"""What each step adds to the context: reasoning, text, tool args, tool outputs (chars)."""
import collections, glob, json, os, statistics, sys

def karox(path):
    out = collections.Counter(); sizes = collections.defaultdict(list); steps = 0
    names = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("kind") != "message":
            continue
        m = r["message"]
        if m.get("role") == "assistant":
            steps += 1
            out["reasoning"] += len(m.get("reasoning") or "")
            out["text"] += len(m.get("content") or "")
            for c in m.get("tool_calls") or []:
                out["args"] += len(c.get("arguments") or "")
                names[c["id"]] = c["name"]
        elif m.get("role") == "tool":
            n = len(m.get("content") or "")
            out["results"] += n
            sizes[m.get("name") or names.get(m.get("tool_call_id"), "?")].append(n)
        elif m.get("role") == "user":
            out["user"] += len(m.get("content") or "")
    return steps, out, sizes

def opencode(path):
    out = collections.Counter(); sizes = collections.defaultdict(list); steps = 0
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t = e.get("type"); p = e.get("part") or {}
        if t == "step_finish":
            steps += 1
        elif t == "reasoning":
            out["reasoning"] += len(p.get("text") or "")
        elif t == "text":
            out["text"] += len(p.get("text") or "")
        elif t == "tool_use":
            st = p.get("state") or {}
            out["args"] += len(json.dumps(st.get("input") or {}, ensure_ascii=False))
            o = st.get("output")
            n = len(o) if isinstance(o, str) else len(json.dumps(o, ensure_ascii=False)) if o is not None else 0
            out["results"] += n
            sizes[p.get("tool") or "?"].append(n)
    return steps, out, sizes

def show(label, items):
    steps = sum(s for s, _, _ in items); tot = collections.Counter(); sizes = collections.defaultdict(list)
    for _, o, sz in items:
        tot.update(o)
        for k, v in sz.items():
            sizes[k] += v
    if not steps:
        return
    print(f"{label}: steps {steps}; per step chars: reasoning {tot['reasoning']/steps:.0f}, text {tot['text']/steps:.0f}, args {tot['args']/steps:.0f}, results {tot['results']/steps:.0f}  => total/step {(tot['reasoning']+tot['text']+tot['args']+tot['results'])/steps:.0f}")
    for k, v in sorted(sizes.items(), key=lambda kv: -sum(kv[1]))[:6]:
        v2 = sorted(v)
        print(f"    {k:12} n={len(v):5} mean {statistics.mean(v):7.0f} median {statistics.median(v):6.0f} p90 {v2[int(len(v2)*0.9)]:7.0f} max {v2[-1]:7.0f}  share of results {sum(v)/max(tot['results'],1):.0%}  >20k: {sum(1 for x in v if x>20000)}")

root = sys.argv[1]
k = [karox(p) for p in glob.glob(os.path.join(root, "**", "session.jsonl"), recursive=True) if ".review" not in p and ".agent-" not in p]
o = [opencode(p) for p in glob.glob(os.path.join(root, "**", "opencode.txt"), recursive=True)]
show("karox6", k); show("opencode_v2", o)
