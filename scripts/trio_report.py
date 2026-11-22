"""Per-task, per-arm report of a downloaded hard12 run, with the validity rule applied.

    python3 scripts/trio_report.py <run dir> [--json out.json]

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
OpenCode's reasoning tokens).
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


def main() -> None:
    root = sys.argv[1]
    trials: dict[str, dict[str, dict]] = collections.defaultdict(dict)
    for path in glob.glob(os.path.join(root, "**", "result.json"), recursive=True):
        trial_dir = os.path.dirname(path)
        if "__" not in os.path.basename(trial_dir):
            continue
        r = _load(path)
        arm = NAMES.get((r.get("agent_info") or {}).get("name"), (r.get("agent_info") or {}).get("name", "?"))
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
        timed_out = "timeout" in text or reason.startswith("time")
        trials[task][arm] = {"reward": float(reward), "provider_end": provider_end, "timed_out": timed_out}

    use: dict[str, dict[str, collections.Counter]] = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for path in glob.glob(os.path.join(root, "**", "audit-*.jsonl"), recursive=True):
        with open(path, encoding="utf-8") as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                c = use[str(e.get("task_id", ""))][str(e.get("harness"))]
                c["calls"] += 1
                if e.get("status") == "success":
                    c["ok"] += 1
                    for k in ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens"):
                        c[k] += e.get(k) or 0
                    c["model_s"] += e.get("latency_s") or 0

    arms = sorted({a for t in trials.values() for a in t})
    solved_all, solved_valid = collections.Counter(), collections.Counter()
    totals: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    valid_tasks, rows = 0, []
    for task in sorted(trials):
        t, u = trials[task], use.get(task, {})
        void = []
        for a in arms:
            if a not in t:
                void.append(f"{a}:missing")
                continue
            c = u.get(a, collections.Counter())
            refused = (c["calls"] - c["ok"]) / c["calls"] if c["calls"] else 0.0
            if t[a]["reward"] < 1 and not c["calls"]:  # never reached the model: setup/infra
                void.append(f"{a}:no-calls")
            elif t[a]["provider_end"]:
                void.append(f"{a}:provider-end")
            elif refused > 0.5 and t[a]["timed_out"]:
                void.append(f"{a}:waited+timeout")
        ok = not void
        valid_tasks += ok
        for a in arms:
            got = int(t.get(a, {}).get("reward", 0) >= 1)
            solved_all[a] += got
            if ok:
                solved_valid[a] += got
            totals[a].update(u.get(a, {}))
        rows.append({"task": task, **{a: int(t.get(a, {}).get("reward", 0) >= 1) for a in arms}, "void": void})
        marks = " ".join(f"{a[:8]}={int(t.get(a, {}).get('reward', 0) >= 1)}" for a in arms)
        print(f"{task[:36]:36} {marks}  {'VOID ' + ','.join(void) if void else 'ok'}")
    print(f"\nvalid tasks {valid_tasks}/{len(trials)}")
    print("solved on valid tasks:", dict(solved_valid))
    print("solved on all tasks  :", dict(solved_all))
    for a in arms:
        c = totals[a]
        refused = (c["calls"] - c["ok"]) / c["calls"] if c["calls"] else 0
        print(
            f"{a:17} ok calls {c['ok']:5} (refused {refused:.0%})  in {c['input_tokens'] / 1e6:6.1f}M  "
            f"out {c['output_tokens'] / 1e3:6.0f}k  reasoning {c['reasoning_tokens'] / 1e3:6.0f}k  "
            f"model {c['model_s'] / 3600:5.1f} h"
        )
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        with open(out, "w", encoding="utf-8") as f:
            json.dump({"rows": rows, "valid_tasks": valid_tasks, "solved_valid": solved_valid,
                       "solved_all": solved_all}, f, indent=1)


if __name__ == "__main__":
    main()
