"""Per-step reasoning by step category for karox6 sessions and opencode logs of a run dir."""
import collections, glob, json, os, statistics, sys

EDIT = {"edit", "write", "apply_patch", "multiedit", "patch"}
SHELL = {"bash", "pwsh", "shell", "run_code"}
LOOK = {"read", "grep", "glob", "list", "ls", "job_output", "job_list"}

def cat(names):
    names = {n.lower() for n in names}
    if not names:
        return "final"
    if names & EDIT:
        return "edit"
    if names & SHELL:
        return "shell"
    if names & LOOK:
        return "look"
    return "other"

def karox_steps(path):
    steps = []
    usage = []
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if r.get("kind") == "message" and r["message"].get("role") == "assistant":
            m = r["message"]
            calls = m.get("tool_calls") or []
            steps.append({
                "cat": cat([c["name"] for c in calls]),
                "tools": [c["name"] for c in calls],
                "rchars": len(m.get("reasoning") or ""),
                "vchars": len(m.get("content") or "") + sum(len(c.get("arguments") or "") for c in calls),
                "argchars": sum(len(c.get("arguments") or "") for c in calls),
                "ncalls": len(calls),
                "reasoning": m.get("reasoning") or "",
            })
        elif r.get("kind") == "usage" and r.get("step"):
            usage.append(r)
    # attach usage by order when counts match
    if len(usage) == len(steps):
        for s, u in zip(steps, usage):
            s["rtok"] = (u.get("usage") or {}).get("reasoning_tokens", 0)
            s["otok"] = (u.get("usage") or {}).get("output_tokens", 0)
            s["itok"] = (u.get("usage") or {}).get("input_tokens", 0)
    return steps

def opencode_steps(path):
    steps, cur = [], None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        t = e.get("type")
        p = e.get("part") or {}
        if t == "step_start":
            cur = {"tools": [], "rchars": 0, "vchars": 0, "argchars": 0, "ncalls": 0, "reasoning": ""}
        elif cur is None:
            continue
        elif t == "reasoning":
            cur["rchars"] += len(p.get("text") or "")
            cur["reasoning"] += p.get("text") or ""
        elif t == "text":
            cur["vchars"] += len(p.get("text") or "")
        elif t == "tool_use":
            cur["tools"].append(p.get("tool") or "?")
            a = json.dumps((p.get("state") or {}).get("input") or {}, ensure_ascii=False)
            cur["argchars"] += len(a)
            cur["vchars"] += len(a)
            cur["ncalls"] += 1
        elif t == "step_finish":
            tok = p.get("tokens") or {}
            cur["rtok"] = tok.get("reasoning", 0)
            cur["otok"] = tok.get("output", 0) + tok.get("reasoning", 0)
            cur["itok"] = tok.get("input", 0) + ((tok.get("cache") or {}).get("read", 0))
            cur["cat"] = cat(cur["tools"])
            steps.append(cur)
            cur = None
    return steps

def summarize(label, all_steps):
    by = collections.defaultdict(list)
    for s in all_steps:
        by[s["cat"]].append(s)
    n = len(all_steps)
    tot_r = sum(s["rchars"] for s in all_steps)
    tot_v = sum(s["vchars"] for s in all_steps)
    print(f"{label}: steps {n}, reasoning chars {tot_r} ({tot_r/max(n,1):.0f}/step), visible chars {tot_v} ({tot_v/max(n,1):.0f}/step), calls/step {sum(s['ncalls'] for s in all_steps)/max(n,1):.2f}")
    for c in ("look", "shell", "edit", "final", "other"):
        ss = by.get(c, [])
        if not ss:
            continue
        r = [s["rchars"] for s in ss]
        print(f"   {c:6} steps {len(ss):5} ({len(ss)/n:4.0%})  reasoning/step mean {statistics.mean(r):7.0f} median {statistics.median(r):6.0f} p90 {sorted(r)[int(len(r)*0.9)]:6.0f}  share of reasoning {sum(r)/max(tot_r,1):4.0%}  args/step {statistics.mean([s['argchars'] for s in ss]):6.0f}")
    big = sorted(all_steps, key=lambda s: -s["rchars"])[: max(n // 20, 1)]
    print(f"   top 5% steps hold {sum(s['rchars'] for s in big)/max(tot_r,1):.0%} of reasoning; their cats: {dict(collections.Counter(s['cat'] for s in big))}")

root = sys.argv[1]
k, o = [], []
for path in glob.glob(os.path.join(root, "**", "session.jsonl"), recursive=True):
    if ".review" in path or ".agent-" in path:
        continue
    k += karox_steps(path)
for path in glob.glob(os.path.join(root, "**", "opencode.txt"), recursive=True):
    o += opencode_steps(path)
summarize("karox6", k)
summarize("opencode_v2", o)
