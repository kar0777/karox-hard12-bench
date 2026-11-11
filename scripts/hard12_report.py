"""HARD12 report over every run: one uniform re-grade of every trial from saved
verifier logs, plus gateway-audited tokens and agent wall time. Same rules for
every arm and every repeat.

    python3 hard12_report.py  ->  /home/ekono/hard12/HARD12_RESULTS.{json,md}

Jobs: hard12-<tag>-<NN>[b]-<task>; tag 20261110 = first night (KaroX wheel v14),
rep* = OpenCode/DSH repeats, k<ver>* = KaroX candidate wheel <ver>.

Grading (identical for all arms):
  * test id matched as fixed string; pytest -rA truncates parametrised ids at
    the first space, so an id with "[" but no "]" is matched as a line prefix;
  * P2P tests that fail in EVERY trial of a task (all arms, all repeats) are
    environment failures (e.g. need network in the verifier) and are excluded;
  * solved = every F2P passes and no remaining P2P regresses.
"""
import datetime as dt
import glob
import json
import os
import re
from collections import defaultdict
from pathlib import Path

JOBS = Path(os.environ["H12_JOBS"])
VAL = Path(os.environ["H12_VAL"])
AUDIT = Path(os.environ["H12_AUDIT"])
ARM = {"karo": "KaroX 5", "opencode-v2-hard12": "OpenCode 2.2.7", "deepseek-harness-hard12": "DeepSeek Harness"}
GW = {"KaroX 5": "karox5", "OpenCode 2.2.7": "opencode_v2", "DeepSeek Harness": "deepseek_harness"}
JOB_RE = re.compile(r"^hard12-(?P<tag>[a-z0-9]+)-(?P<n>\d\d)b?-(?P<name>.+)$")

val = {}
for line in VAL.read_text().splitlines():
    r = json.loads(line)
    if r.get("valid"):
        val[r["key"]] = r
tasks = [l.split() for l in Path(os.environ["H12_TASKS"]).read_text().splitlines() if l.strip()]


def variant(arm, tag):
    if arm != "KaroX 5":
        return arm
    return "KaroX 5 (v14)" if tag == "20261110" else f"KaroX 5 ({tag})"


def passed_fn(lines):
    def passed(i):
        p = "PASSED " + i
        trunc = "[" in i and not i.endswith("]")
        return any(l.startswith(p) and (trunc or l[len(p):] == "" or l[len(p):].startswith(" ")) for l in lines)
    return passed


# Gateway tokens per (job label, gateway arm): context run_id = "<label>-<arm>".
tokens = defaultdict(lambda: {"calls": 0, "input": 0, "cached": 0, "output": 0})
for line in AUDIT.read_text(errors="replace").splitlines():
    try:
        r = json.loads(line)
    except ValueError:
        continue
    if r.get("status") != "success" or not (r.get("task_id") or "").startswith("h12-"):
        continue
    t = tokens[(r.get("run_id") or "", r.get("harness"))]
    t["calls"] += 1
    t["input"] += r.get("input_tokens") or 0
    t["cached"] += r.get("cached_input_tokens") or 0
    t["output"] += r.get("output_tokens") or 0

trials = []  # one per finished trial
for job in sorted(JOBS.glob("hard12-*")):
    m = JOB_RE.match(job.name)
    if not m:
        continue
    n = int(m.group("n"))
    key = tasks[n - 1][0]
    for res in sorted(job.glob("*/result.json")):
        d = json.loads(res.read_text())
        arm = ARM.get((d.get("agent_info") or {}).get("name"))
        log = res.parent / "verifier" / "eval_tests.log"
        if arm is None or not log.is_file():
            continue
        ex = d.get("agent_execution") or {}
        try:
            wall = (dt.datetime.fromisoformat(ex["finished_at"]) - dt.datetime.fromisoformat(ex["started_at"])).total_seconds()
        except (KeyError, TypeError, ValueError):
            wall = None
        trials.append({"n": n, "task": key, "job": job.name, "tag": m.group("tag"), "arm": arm,
                       "variant": variant(arm, m.group("tag")), "wall_s": wall,
                       "lines": log.read_text(errors="replace").splitlines()})

rows = []
for n, (key, _) in enumerate(tasks, 1):
    v = val[key]
    f2p = [i for i in v["f2p"] if "::" in i]
    p2p = [i for i in v["p2p"] if "::" in i]
    mine = [t for t in trials if t["n"] == n]
    fails = [{i for i in p2p if not passed_fn(t["lines"])(i)} for t in mine]
    env_fail = set.intersection(*fails) if fails else set()
    for t, f in zip(mine, fails):
        ok = passed_fn(t["lines"])
        f2p_ok = sum(ok(i) for i in f2p)
        regress = len(f - env_fail)
        rows.append({k: t[k] for k in ("n", "task", "job", "tag", "arm", "variant", "wall_s")} |
                    {"solved": f2p_ok == len(f2p) and regress == 0, "f2p_passed": f2p_ok,
                     "f2p_total": len(f2p), "p2p_regressions": regress, "p2p_env_excluded": len(env_fail)})

# Tokens are per job+arm (repeats inside one job share a run id): spread evenly.
per_job = defaultdict(int)
for r in rows:
    per_job[(r["job"], r["arm"])] += 1
for r in rows:
    tk = tokens[(f"{r['job']}-{GW[r['arm']]}", GW[r["arm"]])]
    share = per_job[(r["job"], r["arm"])]
    for k, val_ in tk.items():
        r[f"tok_{k}"] = val_ / share

out = Path(os.environ["H12_OUT"])
(out / "HARD12_RESULTS.json").write_text(json.dumps(rows, indent=1) + "\n")
variants = sorted({r["variant"] for r in rows}, key=lambda s: (not s.startswith("KaroX"), s))
md = ["# HARD12 results (12 fresh post-2026-10-18 tasks, DeepSeek-V4.1-Flash-1017, same gateway)", "",
      "Cell = solved trials / trials (F2P passed summed over trials).", "",
      "| # | task | " + " | ".join(variants) + " |", "|---|---|" + "---|" * len(variants)]
for n, (key, _) in enumerate(tasks, 1):
    cells = []
    for a in variants:
        rs = [x for x in rows if x["n"] == n and x["variant"] == a]
        if not rs:
            cells.append("—")
            continue
        reg = sum(x["p2p_regressions"] for x in rs)
        cells.append(f"{sum(x['solved'] for x in rs)}/{len(rs)} ({sum(x['f2p_passed'] for x in rs)}/"
                     f"{sum(x['f2p_total'] for x in rs)}){' reg' + str(reg) if reg else ''}")
    md.append(f"| {n} | {key} | " + " | ".join(cells) + " |")
md += ["", "| variant | trials | solved | solve rate | solved per 12 tasks | F2P passed | P2P regressions | "
       "input tok / trial | output tok / trial | agent min / trial |",
       "|---|---|---|---|---|---|---|---|---|---|"]
for a in variants:
    rs = [r for r in rows if r["variant"] == a]
    k = len(rs)
    s = sum(r["solved"] for r in rs)
    md.append(f"| {a} | {k} | {s} | {s / k:.0%} | {12 * s / k:.1f} | "
              f"{sum(r['f2p_passed'] for r in rs)}/{sum(r['f2p_total'] for r in rs)} | "
              f"{sum(r['p2p_regressions'] for r in rs)} | {sum(r['tok_input'] for r in rs) / k:,.0f} | "
              f"{sum(r['tok_output'] for r in rs) / k:,.0f} | {sum(r['wall_s'] or 0 for r in rs) / 60 / k:.1f} |")
(out / "HARD12_RESULTS.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
