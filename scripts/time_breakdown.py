"""Per-trial time breakdown for every arm: where the wall time went.

python3 scripts/time_breakdown.py JOBS_DIR AUDIT_JSONL OUT_PREFIX
Writes OUT_PREFIX.csv and OUT_PREFIX.md. Per trial: Harbor phases (env setup, agent
setup, agent run, verifier), model time from the gateway audit (sum of call latencies,
time to first token), failed calls and 429s, an upstream_failed flag (the last
successful call came long before the agent ended, or failed calls dominate), tool time
(karox6 from its events, opencode from its part timings, others = agent run - model),
and hidden-test counts from verifier/ctrf.json.
"""

import csv
import glob
import json
import os
import re
import statistics
import sys
from collections import defaultdict
from datetime import datetime

ARM = {"karox6-hard12": "karox6", "karox6b-hard12": "karox6b", "opencode-v2-hard12": "opencode_v2",
       "deepseek-harness-hard12": "deepseek_harness", "karo-hard12": "karox5"}


def epoch(text):
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def phase(result, key):
    p = result.get(key) or {}
    a, b = epoch(p.get("started_at")), epoch(p.get("finished_at"))
    return round(b - a, 1) if a and b else None


def load_audit(path):
    calls = defaultdict(list)
    if not os.path.exists(path):
        return calls
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        calls[(r.get("task_id"), r.get("harness"))].append(r)
    return calls


def karox_tool_s(trial):
    total = 0.0
    for path in glob.glob(f"{trial}/agent/karox6.jsonl"):
        for line in open(path, encoding="utf-8", errors="replace"):
            if '"tool_finished"' in line:
                try:
                    total += (json.loads(line).get("duration_ms") or 0) / 1000
                except json.JSONDecodeError:
                    pass
    return round(total, 1)


def opencode_tool_s(trial):
    total = 0.0
    for path in glob.glob(f"{trial}/agent/opencode.txt"):
        for line in open(path, encoding="utf-8", errors="replace"):
            if '"type":"tool_use"' not in line:
                continue
            m = re.search(r'"time":\{"start":(\d+),"end":(\d+)', line)
            if m:
                total += (int(m.group(2)) - int(m.group(1))) / 1000
    return round(total, 1)


def ctrf(trial):
    path = f"{trial}/verifier/ctrf.json"
    if not os.path.exists(path):
        return None, None
    try:
        tests = json.load(open(path, encoding="utf-8")).get("results", {}).get("tests", [])
    except Exception:
        return None, None
    passed = sum(1 for t in tests if t.get("status") == "passed")
    return passed, len(tests)


def main():
    jobs, audit_path, prefix = sys.argv[1:4]
    calls = load_audit(audit_path)
    rows = []
    for path in sorted(glob.glob(f"{jobs}/*/*/result.json")):
        trial = os.path.dirname(path)
        try:
            r = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        arm = ARM.get((r.get("agent_info") or {}).get("name") or "", "other")
        task = (r.get("task_name") or "").split("/")[-1]
        cs = calls.get((task, arm), [])
        ok = [c for c in cs if c.get("status") == "success"]
        llm = sum(c.get("latency_s") or 0 for c in ok)
        ttfts = [c["ttft_s"] for c in ok if isinstance(c.get("ttft_s"), (int, float))]
        agent_s = phase(r, "agent_execution")
        agent_end = epoch((r.get("agent_execution") or {}).get("finished_at"))
        last_ok = max((epoch(c.get("ts")) or 0 for c in ok), default=0)
        failed = len(cs) - len(ok)
        last = max(cs, key=lambda c: epoch(c.get("ts")) or 0) if cs else None
        ended_on_failure = bool(
            last is not None and last.get("status") != "success" and agent_end
            and agent_end - (epoch(last.get("ts")) or 0) < 120
        )
        r429 = sum(1 for c in cs if "RateLimit" in (c.get("error") or ""))
        if arm == "karox6":
            tool = karox_tool_s(trial)
        elif arm == "opencode_v2":
            tool = opencode_tool_s(trial)
        else:
            tool = round(agent_s - llm, 1) if agent_s is not None else None
        passed, total = ctrf(trial)
        rows.append({
            "task": task,
            "arm": arm,
            "reward": ((r.get("verifier_result") or {}).get("rewards") or {}).get("reward"),
            "exception": (r.get("exception_info") or {}).get("exception_type") or "",
            "env_setup_s": phase(r, "environment_setup"),
            "agent_setup_s": phase(r, "agent_setup"),
            "agent_s": agent_s,
            "verifier_s": phase(r, "verifier"),
            "llm_s": round(llm, 1),
            "tool_s": tool,
            "other_s": round(agent_s - llm - tool, 1) if agent_s is not None and tool is not None
            and arm in ("karox6", "opencode_v2") else None,
            "calls": len(ok),
            "failed_calls": failed,
            "r429": r429,
            "ttft_med_s": round(statistics.median(ttfts), 2) if ttfts else None,
            "out_tok": sum(c.get("output_tokens") or 0 for c in ok),
            "reason_tok": sum(c.get("reasoning_tokens") or 0 for c in ok),
            "idle_tail_s": round(agent_end - last_ok, 1) if agent_end and last_ok else None,
            # The provider, not the agent, ended the trial: the agent stopped within 2 min
            # of a failed call, no success in its last 10 min, or failures outnumber
            # successes.
            "upstream_failed": bool(cs) and (ended_on_failure or
                (agent_end and last_ok and agent_end - last_ok > 600) or failed > len(ok)
            ),
            "tests_passed": passed,
            "tests_total": total,
        })
    if not rows:
        print("no trials")
        return
    with open(prefix + ".csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    cols = ["task", "arm", "reward", "agent_s", "llm_s", "tool_s", "calls", "failed_calls",
            "r429", "ttft_med_s", "out_tok", "upstream_failed", "tests_passed", "tests_total"]
    with open(prefix + ".md", "w", encoding="utf-8") as f:
        f.write("## Time breakdown per trial\n\n| " + " | ".join(cols) + " |\n|"
                + "---|" * len(cols) + "\n")
        for row in sorted(rows, key=lambda x: (x["task"], x["arm"])):
            f.write("| " + " | ".join("" if row[c] is None else str(row[c]) for c in cols) + " |\n")
        f.write("\n| arm | trials | solved | agent_s sum | llm_s sum | tool_s sum | upstream_failed |\n"
                "|---|---|---|---|---|---|---|\n")
        for arm in sorted({x["arm"] for x in rows}):
            rs = [x for x in rows if x["arm"] == arm]
            s = lambda k: round(sum(x[k] or 0 for x in rs))  # noqa: E731
            f.write(f"| {arm} | {len(rs)} | {sum(1 for x in rs if x['reward'] == 1)} | "
                    f"{s('agent_s')} | {s('llm_s')} | {s('tool_s')} | "
                    f"{sum(1 for x in rs if x['upstream_failed'])} |\n")
    print(len(rows), "trials ->", prefix + ".csv/.md")


if __name__ == "__main__":
    main()
