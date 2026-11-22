"""How often an agent's reasoning argues about the scope of its fix, per arm.

    python scopewords.py <run dir> [<run dir> ...] [--show N]

Counts, per trial, the reasoning passages that weigh the scope of the change: the words of
KaroX's own prompt rules ("smallest", "contract", "broaden") and the general ones ("scope",
"minimal", "not asked"). Reads KaroX session logs and DSH's dsh.jsonl. --show N prints N
characters around every match of the prompt's words (for reading a decision, not a count).
"""
import collections
import glob
import json
import os
import re
import sys

GROUPS = {
    "prompt: smallest": re.compile(r"smallest (?:general )?change", re.I),
    "prompt: contract/broaden": re.compile(
        r"broaden|exact contract|(?:the|task) contract|contract (?:says|is)", re.I),
    "scope": re.compile(r"(?:expand|out of|beyond(?: the)?|widen(?:ing)?|outside(?: the)?) scope|"
                        r"scope creep|not (?:in|part of) (?:the )?scope|not scope\b", re.I),
    "minimal": re.compile(r"\bminimal(?:ly)?\b", re.I),
    "not asked": re.compile(r"(?:not|n't|isn't|wasn't) (?:asked|requested|required|needed|"
                            r"necessary|mentioned)|more than asked", re.I),
}
PROMPT_WORDS = ("prompt: smallest", "prompt: contract/broaden")


def karox_blocks(trial_dir):
    out = []
    pattern = os.path.join(trial_dir, "agent", "karox6", "sessions", "*", "session.jsonl")
    for path in glob.glob(pattern):
        for line in open(path, encoding="utf-8", errors="replace"):
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if row.get("kind") == "message" and row["message"].get("role") == "assistant":
                out.append(row["message"].get("reasoning") or "")
    return out


def dsh_blocks(trial_dir):
    out, cur = [], []
    for line in open(os.path.join(trial_dir, "agent", "dsh.jsonl"), encoding="utf-8",
                     errors="replace"):
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if row.get("type") == "status" and row.get("phase") == "step_start":
            if cur:
                out.append("\n".join(cur))
            cur = []
        elif row.get("type") == "thinking":
            cur.append(row.get("text") or "")
    if cur:
        out.append("\n".join(cur))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    runs = [a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()]
    show = int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 0
    trials = collections.defaultdict(list)
    for run in runs:
        for trial_dir in sorted(glob.glob(os.path.join(run, "trial-*", "jobs", "*", "*__*"))):
            log = os.path.join(trial_dir, "agent", "karox6.jsonl")
            if os.path.exists(log):
                try:  # karox6 or karox6b: the model alias of the run
                    first = json.loads(open(log, encoding="utf-8", errors="replace").readline())
                except ValueError:
                    first = {}
                arm = str(first.get("model") or "hard12-karox6").removeprefix("hard12-")
                blocks = karox_blocks(trial_dir)
            elif os.path.exists(os.path.join(trial_dir, "agent", "dsh.jsonl")):
                arm, blocks = "deepseek_harness", dsh_blocks(trial_dir)
            else:
                continue
            if len(blocks) <= 5:  # ended on a provider error
                continue
            job = os.path.basename(os.path.dirname(trial_dir))
            hits = {name: sum(len(rx.findall(b)) for b in blocks) for name, rx in GROUPS.items()}
            trials[arm].append((job, len(blocks), sum(len(b) for b in blocks), hits))
            if show and arm.startswith("karox6"):
                for i, block in enumerate(blocks, 1):
                    for name in PROMPT_WORDS:
                        for m in GROUPS[name].finditer(block):
                            a, b = max(0, m.start() - show), min(len(block), m.end() + show)
                            print(f"{job} [{i}] ...{block[a:b]}...".replace("\n", " "))
    print("arm | trials | reasoning chars per trial | " + " | ".join(
        f"{name}: trials with it, mentions per trial" for name in GROUPS))
    for arm, rows in trials.items():
        cells = []
        for name in GROUPS:
            with_it = sum(1 for _, _, _, hits in rows if hits[name])
            mean = sum(hits[name] for _, _, _, hits in rows) / len(rows)
            cells.append(f"{with_it}/{len(rows)}, {mean:.1f}")
        chars = sum(c for _, _, c, _ in rows) / len(rows)
        print(f"{arm} | {len(rows)} | {chars:.0f} | " + " | ".join(cells))


if __name__ == "__main__":
    main()
