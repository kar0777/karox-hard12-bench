"""One line per KaroX trial of a downloaded run: ending, steps, usage, tool mix, errors.

    python karox_ends.py <run dir> [<run dir> ...]
"""
import collections
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for root in sys.argv[1:]:
    for path in sorted(glob.glob(os.path.join(root, "**", "karox6.jsonl"), recursive=True)):
        trial = os.path.basename(os.path.dirname(os.path.dirname(path)))
        result = os.path.join(os.path.dirname(os.path.dirname(path)), "result.json")
        reward = "?"
        arm = "?"
        if os.path.exists(result):
            r = json.load(open(result, encoding="utf-8"))
            reward = ((r.get("verifier_result") or {}).get("rewards") or {}).get("reward")
            arm = (r.get("agent_info") or {}).get("name")
        tools = collections.Counter()
        errs = collections.Counter()
        other = collections.Counter()
        fin = {}
        steps = 0
        retries = 0
        finish = collections.Counter()
        notices = []
        for line in open(path, encoding="utf-8"):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            t = e.get("type")
            if t == "tool_finished":
                tools[e["name"]] += 1
                if e.get("is_error"):
                    errs[e["name"]] += 1
            elif t == "usage":
                steps = max(steps, e.get("step", 0))
                retries += e.get("retries") or 0
                finish[e.get("finish_reason")] += 1
            elif t == "run_finished":
                fin = e
            elif t not in ("assistant_message", "tool_started", "run_started"):
                other[t] += 1
                if t in ("notice", "harness_notice", "warning", "compaction", "retry"):
                    notices.append(json.dumps(e, ensure_ascii=False)[:300])
        u = fin.get("usage") or {}
        stderr = os.path.join(os.path.dirname(path), "karox6.stderr.txt")
        err_size = os.path.getsize(stderr) if os.path.exists(stderr) else -1
        print(f"{trial[:44]:44} {arm} reward={reward} status={fin.get('status')} reason={fin.get('reason')} "
              f"steps={steps} in={u.get('input_tokens')} cached={u.get('cached_tokens')} out={u.get('output_tokens')} "
              f"reas={u.get('reasoning_tokens')} retries={retries} finish={dict(finish)} tools={dict(tools)} "
              f"tool_errs={dict(errs)} other={dict(other)} stderr={err_size}")
        for n in notices[:8]:
            print("    ", n)
