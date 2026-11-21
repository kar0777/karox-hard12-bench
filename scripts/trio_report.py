"""Per-task, per-arm report of downloaded hard12 runs, with the validity rule applied.

    python3 scripts/trio_report.py <run dir> [<run dir> ...] [--json out.json] [--md out.md]
                                   [--price in,cached,out]

Validity (pre-registered 2026-11-21 for the Dahl lane, applies to every lane): a refused
request that the gateway retried and that then succeeded costs the agent about a second
and is not a failure. A TRIAL is void only when the provider hurt the agent itself:
  * the trial ended unsolved on a provider error (KaroX: its run_finished reason starts
    with rate_limit / server / quota; other CLIs: Harbor's exception type names a rate
    limit, capacity or API error), or
  * refused requests made up more than half of that arm's requests AND the agent hit
    its time limit (the waiting may have cost it the task).
A TASK counts for the comparison only when every arm's trial on it is valid (same
conditions for all). Tokens and model time come from the gateway audit (successful
calls only): one counter for every arm, unlike the CLIs' own logs (Harbor omits
OpenCode's reasoning tokens). Agent time is Harbor's agent_execution phase. The
cost-equivalent prices the audit tokens at one list for every arm (default: the W&B list
for DeepSeek-V4.1-Flash used by karox6-bench-data/compare.py; `--price in,cached,out`
in USD per 1M tokens overrides it). Several run directories are pooled (a task seen
twice keeps its last trial per arm). `--md FILE` also writes the tables as Markdown.
"""

from __future__ import annotations

import collections
import glob
import json
import os
import sys

NAMES = {
    "karox6-hard12": "karox6",
    "karox6b-hard12": "karox6b",
    "opencode-v2-hard12": "opencode_v2",
    "deepseek-harness-hard12": "deepseek_harness",
}
PROVIDER_WORDS = ("ratelimit", "rate_limit", "rate limit", "capacity", "apierror", "api error")
PRICE = {"input": 0.13, "cached": 0.002, "output": 0.65}  # USD per 1M tokens
TOKEN_KEYS = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens")


def _seconds(phase: dict | None) -> float:
    from datetime import datetime

    try:
        start = datetime.fromisoformat(str((phase or {})["started_at"]).replace("Z", "+00:00"))
        end = datetime.fromisoformat(str((phase or {})["finished_at"]).replace("Z", "+00:00"))
    except (KeyError, ValueError):
        return 0.0
    return max((end - start).total_seconds(), 0.0)


def _cost(c: collections.Counter) -> float:
    fresh = max(c["input_tokens"] - c["cached_input_tokens"], 0)
    return (fresh * PRICE["input"] + c["cached_input_tokens"] * PRICE["cached"]
            + c["output_tokens"] * PRICE["output"]) / 1e6


def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _karox_reason(trial_dir: str) -> str:
    for path in glob.glob(os.path.join(trial_dir, "agent", "**", "karox6.jsonl"), recursive=True):
        reason = ""
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    event = json.loads(line)
                except ValueError:
                    continue
                if event.get("type") == "run_finished":
                    reason = f"{event.get('status')}:{event.get('reason') or ''}"
        return reason
    return ""


def _flag(name: str) -> str | None:
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def main() -> None:
    skip = {i + 1 for i, a in enumerate(sys.argv) if a in ("--json", "--md", "--price")}
    roots = [a for i, a in enumerate(sys.argv) if i and i not in skip and not a.startswith("--")]
    if not roots:
        sys.exit(__doc__)
    if _flag("--price"):
        PRICE.update(zip(("input", "cached", "output"),
                         (float(x) for x in str(_flag("--price")).split(","))))
    trials: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    versions: dict[str, set[str]] = collections.defaultdict(set)
    seen_dirs: set[str] = set()
    for root in roots:
        for path in sorted(glob.glob(os.path.join(root, "**", "result.json"), recursive=True)):
            trial_dir = os.path.dirname(path)
            name = os.path.basename(trial_dir)
            if "__" not in name or name in seen_dirs:
                continue  # a job-level result, or the same trial under alljobs/ and trial-*/
            seen_dirs.add(name)
            r = _load(path)
            info = r.get("agent_info") or {}
            arm = NAMES.get(info.get("name"), info.get("name", "?"))
            if info.get("version"):
                versions[arm].add(str(info["version"]).strip())
            task = str(r.get("task_name", "?")).split("/")[-1]
            exc = r.get("exception_info") or {}
            # The exception TYPE only: its message carries the agent's log tail, where retried
            # (harmless) 429s show up in trials that went on and solved the task.
            text = str(exc.get("exception_type", "")).lower()
            reason = _karox_reason(trial_dir) if arm.startswith("karox6") else ""
            reward = ((r.get("verifier_result") or {}).get("rewards") or {}).get("reward") or 0
            if reason:  # KaroX names its own ending; Harbor's type is a guess from the log tail
                provider_end = reason.split(":", 1)[-1].startswith(("rate_limit", "server", "quota"))
            else:
                provider_end = any(w in text for w in PROVIDER_WORDS)
            provider_end = provider_end and float(reward) < 1  # a solved trial was not hurt
            timed_out = "timeout" in text or reason.startswith(("time", "limit:time"))
            trials[task][arm] = {
                "reward": float(reward),
                "provider_end": provider_end,
                "timed_out": timed_out,
                "agent_s": _seconds(r.get("agent_execution")),
                "ended": reason or text or "ok",
            }

    use: dict[str, dict[str, collections.Counter]] = collections.defaultdict(
        lambda: collections.defaultdict(collections.Counter))
    seen_calls: set[tuple] = set()
    ttft: dict[str, dict[str, list[float]]] = collections.defaultdict(
        lambda: collections.defaultdict(list))
    for root in roots:
        for path in glob.glob(os.path.join(root, "**", "*audit*.jsonl"), recursive=True):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    try:
                        e = json.loads(line)
                    except ValueError:
                        continue
                    key = (e.get("run_id"), e.get("start_epoch"), e.get("ts"),
                           e.get("input_tokens"), e.get("output_tokens"), e.get("status"))
                    if key in seen_calls:
                        continue  # merged and per-job copies of the same audit
                    seen_calls.add(key)
                    c = use[str(e.get("task_id", ""))][str(e.get("harness"))]
                    c["calls"] += 1
                    if e.get("status") == "success":
                        c["ok"] += 1
                        for k in TOKEN_KEYS:
                            c[k] += e.get(k) or 0
                        c["model_s"] += e.get("latency_s") or 0
                        if e.get("ttft_s"):
                            ttft[str(e.get("task_id", ""))][str(e.get("harness"))].append(e["ttft_s"])

    arms = sorted({a for t in trials.values() for a in t})
    solved_all, solved_valid = collections.Counter(), collections.Counter()
    totals: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    valid: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    valid_tasks, rows = 0, []
    first_token: dict[tuple[str, str], list[float]] = collections.defaultdict(list)
    for task in sorted(trials):
        t, u = trials[task], use.get(task, {})
        void = []
        for a in arms:
            if a not in t:
                void.append(f"{a}:missing")
                continue
            c = u.get(a, collections.Counter())
            refused = (c["calls"] - c["ok"]) / c["calls"] if c["calls"] else 0.0
            if t[a]["provider_end"]:
                void.append(f"{a}:provider-end")
            elif refused > 0.5 and t[a]["timed_out"]:
                void.append(f"{a}:waited+timeout")
        ok = not void
        valid_tasks += ok
        for a in arms:
            got = int(t.get(a, {}).get("reward", 0) >= 1)
            solved_all[a] += got
            totals[a].update(u.get(a, {}))
            totals[a]["agent_s"] += t.get(a, {}).get("agent_s", 0.0)
            first_token[("all tasks", a)] += ttft.get(task, {}).get(a, [])
            if ok:
                solved_valid[a] += got
                valid[a].update(u.get(a, {}))
                valid[a]["agent_s"] += t.get(a, {}).get("agent_s", 0.0)
                first_token[("valid tasks", a)] += ttft.get(task, {}).get(a, [])
        rows.append({
            "task": task,
            **{a: int(t.get(a, {}).get("reward", 0) >= 1) for a in arms},
            **{f"{a}_calls": u.get(a, collections.Counter())["ok"] for a in arms},
            **{f"{a}_agent_s": round(t.get(a, {}).get("agent_s", 0.0)) for a in arms},
            "void": void,
        })
        marks = " ".join(f"{a[:8]}={int(t.get(a, {}).get('reward', 0) >= 1)}" for a in arms)
        print(f"{task[:36]:36} {marks}  {'VOID ' + ','.join(void) if void else 'ok'}")
    print(f"\nvalid tasks {valid_tasks}/{len(trials)}")
    print("solved on valid tasks:", dict(solved_valid))
    print("solved on all tasks  :", dict(solved_all))
    print("versions:", {a: sorted(v) for a, v in versions.items()})
    print(f"price list (USD per 1M): {PRICE}")
    summary = {}
    for scope, data in (("valid tasks", valid), ("all tasks", totals)):
        print(f"-- usage on {scope}")
        for a in arms:
            c = data[a]
            refused = (c["calls"] - c["ok"]) / c["calls"] if c["calls"] else 0
            cached = c["cached_input_tokens"] / c["input_tokens"] if c["input_tokens"] else 0
            line = {
                "solved": (solved_valid if scope == "valid tasks" else solved_all)[a],
                "ok_calls": c["ok"],
                "refused": round(refused, 3),
                "input_M": round(c["input_tokens"] / 1e6, 2),
                "cached": round(cached, 3),
                "output_k": round(c["output_tokens"] / 1e3),
                "reasoning_k": round(c["reasoning_tokens"] / 1e3),
                "model_h": round(c["model_s"] / 3600, 2),
                "agent_min": round(c["agent_s"] / 60, 1),
                "cost_usd": round(_cost(c), 3),
            }
            n_tasks = max(valid_tasks if scope == "valid tasks" else len(trials), 1)
            waits = sorted(first_token[(scope, a)])
            line.update({
                "ttft_median_s": round(waits[len(waits) // 2], 2) if waits else None,
                "per_task": {
                    "calls": round(c["ok"] / n_tasks, 1),
                    "input_M": round(c["input_tokens"] / 1e6 / n_tasks, 2),
                    "output_k": round(c["output_tokens"] / 1e3 / n_tasks, 1),
                    "agent_min": round(c["agent_s"] / 60 / n_tasks, 1),
                    "cost_usd": round(_cost(c) / n_tasks, 4),
                },
            })
            summary.setdefault(scope, {})[a] = line
            print(
                f"{a:17} ok calls {c['ok']:5} (refused {refused:.0%})  in {line['input_M']:6.1f}M "
                f"(cached {cached:.0%})  out {line['output_k']:6.0f}k  reasoning "
                f"{line['reasoning_k']:6.0f}k  model {line['model_h']:5.2f} h  agent "
                f"{line['agent_min']:6.1f} min  cost ${line['cost_usd']:.3f}"
            )
            per = line["per_task"]
            print(
                f"{'':17} per task: {per['calls']} calls, {per['input_M']}M in, {per['output_k']}k out, "
                f"{per['agent_min']} min, ${per['cost_usd']}; time to first token (median) "
                f"{line['ttft_median_s']} s"
            )
    if _flag("--json"):
        with open(str(_flag("--json")), "w", encoding="utf-8") as f:
            json.dump({"rows": rows, "valid_tasks": valid_tasks, "tasks": len(trials),
                       "solved_valid": solved_valid, "solved_all": solved_all,
                       "usage": summary, "price": PRICE,
                       "versions": {a: sorted(v) for a, v in versions.items()}}, f, indent=1)
    if _flag("--md"):
        with open(str(_flag("--md")), "w", encoding="utf-8") as f:
            f.write("| task | " + " | ".join(arms) + " | note |\n")
            f.write("|---|" + "---|" * len(arms) + "---|\n")
            for row in rows:
                cells = " | ".join(
                    f"{'solved' if row[a] else 'failed'} ({row[f'{a}_calls']} calls, "
                    f"{row[f'{a}_agent_s'] // 60} min)" for a in arms)
                f.write(f"| {row['task']} | {cells} | {'VOID: ' + ', '.join(row['void']) if row['void'] else ''} |\n")
            for scope, per_arm in summary.items():
                f.write(f"\nUsage on {scope} ({valid_tasks if scope == 'valid tasks' else len(trials)}):\n\n")
                f.write("| arm | solved | ok calls | refused | input M | cached | output k | "
                        "reasoning k | TTFT s | model h | agent min | cost $ | per task: calls / "
                        "min / $ |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
                for a, s in per_arm.items():
                    per = s["per_task"]
                    f.write(f"| {a} | {s['solved']} | {s['ok_calls']} | {s['refused']:.0%} | "
                            f"{s['input_M']} | {s['cached']:.0%} | {s['output_k']} | "
                            f"{s['reasoning_k']} | {s['ttft_median_s']} | {s['model_h']} | "
                            f"{s['agent_min']} | {s['cost_usd']} | {per['calls']} / "
                            f"{per['agent_min']} / {per['cost_usd']} |\n")


if __name__ == "__main__":
    main()
