"""KaroX vs DSH, trial by trial: when the first edit comes, how the change is checked, how
the run ends, and what the diff holds.

    python dshcmp.py <run dir> [<run dir> ...] [--tasks]

A run is split at its first and its last edit of a source file: explore (before the first),
work (first to last), tail (after the last). Steps come from each trial's agent log
(karox6.jsonl / dsh.jsonl), tokens from the gateway audit (the same counter for both arms),
the diff from verifier/agent.diff, missed hidden tests from the verifier. Sizes are never
taken from the logs: DSH's log cuts every tool result at 8k characters. DSH's one request
for a session title is counted as a model call and left out of the phases.
Prints group means; --tasks adds one line per task. No model calls, nothing is written.
"""
import collections
import glob
import json
import os
import re
import statistics
import sys

ARMS = {"karox6": "karox6.jsonl", "deepseek_harness": "dsh.jsonl"}
EDIT_TOOLS = {"edit", "write", "multiedit", "apply_patch", "patch"}
LOOK_TOOLS = {"read", "grep", "glob", "list", "ls"}
TEST_RE = re.compile(
    r"(?<![\w/.-])(pytest|py\.test|tox|nox|unittest|vitest|jest|mocha|go test|cargo test|"
    r"bun test|deno test|npm (?:run )?test|pnpm (?:run )?test|yarn (?:run )?test|"
    r"make (?:test|check)|ctest|rspec|phpunit|node --test)(?![\w-])"
)
RUNNER = r"(?:python[0-9.]*|node|bun|deno|tsx|ts-node|ruby)"
PROBE_RE = re.compile(
    rf"\b{RUNNER}\b[^|;&\n]*?\s(?:-c|-e|-)(?:\s|$)|\b{RUNNER}\b[^\n]*<<|"
    rf"\b{RUNNER}\s+(?:/tmp/\S+|\S*(?:repro|probe|scratch|verify|check_|try_|demo|debug)\S*)"
)
SHELL_EDIT_RE = re.compile(
    r"\bsed\s+(?:-[a-zA-Z]*i|--in-place)|\bgit\s+apply\b|\bpatch\s+-p|\bperl\s+-[a-z]*i|"
    r"(?:cat|tee)\s*>+\s*(?!/tmp)[\w./-]+\s*<<|\.write_text\(|open\([^)]*['\"][wa]['\"]"
)
LOOK_CMD_RE = re.compile(
    r"^\s*(?:cd\s+\S+\s*(?:&&|;)\s*)?(?:cat|head|tail|sed\s+-n|nl|grep|rg|find|ls|wc|tree|"
    r"git\s+(?:log|show|diff|status|grep|blame))\b"
)
TEST_PATH_RE = re.compile(
    r"(?:^|/)(?:tests?|__tests__|spec|testing)/|(?:^|/)test_[^/]*\.py$|_test\.(?:py|go)$|"
    r"\.(?:test|spec)\.[cm]?[jt]sx?$|(?:^|/)conftest\.py$"
)


def args_of(raw):
    if isinstance(raw, dict):
        return raw
    try:
        value = json.loads(raw or "{}")
    except ValueError:
        return {"command": str(raw)}
    return value if isinstance(value, dict) else {}


def path_of(args):
    for key in ("path", "file_path", "filePath", "filename", "file"):
        if isinstance(args.get(key), str):
            return args[key]
    return ""


def kinds(name, args):
    """What one tool call does: look / test / probe / edit (source) / testedit / other."""
    name = (name or "").lower()
    if name in EDIT_TOOLS:
        path = path_of(args)
        if "/tmp/" in path or path.startswith("/tmp"):
            return {"scratch"}
        return {"testedit"} if TEST_PATH_RE.search(path) else {"edit"}
    if name in LOOK_TOOLS:
        return {"look"}
    if name not in ("bash", "pwsh", "shell"):
        return {"other"}
    cmd = str(args.get("command") or args.get("cmd") or "")
    out = set()
    if TEST_RE.search(cmd):
        out.add("test")
    elif PROBE_RE.search(cmd):
        out.add("probe")
    if SHELL_EDIT_RE.search(cmd) and "probe" not in out:
        out.add("edit")
    if not out:
        out.add("look" if LOOK_CMD_RE.search(cmd) else "other")
    return out


def karox_steps(path):
    steps, final = [], ""
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if row.get("type") == "assistant_message":
            steps.append([{"name": call.get("name"), "args": args_of(call.get("arguments"))}
                          for call in row.get("tool_calls") or []])
        elif row.get("type") == "run_finished":
            final = row.get("final_text") or ""
    return steps, final


def dsh_steps(path):
    steps, final = [], ""
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            row = json.loads(line)
        except ValueError:
            continue
        kind = row.get("type")
        if kind == "status" and row.get("phase") == "step_start":
            steps.append([])
        elif kind == "tool_call" and steps:
            steps[-1].append({"name": row.get("tool"), "args": args_of(row.get("input"))})
        elif kind == "final":
            final = row.get("text") or ""
    return steps, final


def diff_stats(path):
    stats = {"src_files": 0, "test_files": 0, "src_added": 0, "test_added": 0}
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return {}
    where = None
    for line in lines:
        if line.startswith("diff --git "):
            name = line.split(" b/", 1)[-1]
            if name.endswith(("package-lock.json", ".lock", "pnpm-lock.yaml")):
                where = None
            else:
                where = "test" if TEST_PATH_RE.search(name) else "src"
                stats[where + "_files"] += 1
        elif line.startswith("+") and not line.startswith("+++") and where:
            stats[where + "_added"] += 1
    return stats


def verdict(trial_dir):
    """(reward, hidden tests not passed) from the verifier's files."""
    reward = missing = None
    try:
        rewards = json.load(open(os.path.join(trial_dir, "result.json"), encoding="utf-8"))
        rewards = (rewards.get("verifier_result") or {}).get("rewards") or {}
    except (OSError, ValueError):
        rewards = {}
    if "reward" in rewards:
        reward = float(rewards["reward"])
    if "f2p_total" in rewards:
        missing = (rewards["f2p_total"] - rewards["f2p_passed"]
                   + rewards.get("p2p_total", 0) - rewards.get("p2p_passed", 0))
    try:
        log = open(os.path.join(trial_dir, "verifier", "eval_missing.log"),
                   encoding="utf-8", errors="replace")
        missing = sum(1 for line in log if line.startswith("NOT PASSED"))
    except OSError:
        pass
    return reward, missing


def step_rows(rows, steps):
    """The audit rows of the agent's steps, in order: without the session-title request."""
    if len(rows) == steps + 1:
        small = min(range(min(3, len(rows))), key=lambda i: rows[i]["input_tokens"] or 0)
        if (rows[small]["input_tokens"] or 0) < 2500:
            return rows[:small] + rows[small + 1:]
    return rows


def trial(agent_dir, arm, audit):
    steps, final = (karox_steps if arm == "karox6" else dsh_steps)(
        os.path.join(agent_dir, ARMS[arm]))
    trial_dir = os.path.dirname(agent_dir)
    job = os.path.basename(os.path.dirname(trial_dir))
    all_rows = audit.get((job, arm), [])
    rows = step_rows(all_rows, len(steps))
    labelled = [[k for call in step for k in kinds(call["name"], call["args"])] for step in steps]
    edits = [i for i, ks in enumerate(labelled) if "edit" in ks]
    first = edits[0] if edits else len(steps)
    last = edits[-1] if edits else len(steps) - 1
    phases = {"explore": (0, first), "work": (first, last + 1), "tail": (last + 1, len(steps))}

    def tokens(key, a=0, b=None):
        return sum(r[key] or 0 for r in rows[a:b])

    def count(kind, a=0, b=None):
        return sum(ks.count(kind) for ks in labelled[a:b])

    reward, missing = verdict(trial_dir)
    calls = [call for step in steps for call in step]
    edited = {path_of(c["args"]) for c in calls
              if (c["name"] or "").lower() in EDIT_TOOLS and "/tmp" not in path_of(c["args"])}
    out = {
        "task": re.sub(r"^hard12-[a-z0-9]+-\d+-", "", job), "arm": arm, "reward": reward,
        "missing": missing, "calls": len(all_rows), "steps": len(steps), "tools": len(calls),
        "first_edit": first + 1,
        "ctx_at_edit": (rows[first]["input_tokens"] or 0) if first < len(rows) else None,
        "first_input": (rows[0]["input_tokens"] or 0) if rows else None,
        "peak_input": max((r["input_tokens"] or 0 for r in rows), default=0),
        "edits": count("edit"), "testedits": count("testedit"),
        "tests": count("test"), "probes": count("probe"), "looks": count("look"),
        "final_chars": len(final), "out": sum(r["output_tokens"] or 0 for r in all_rows),
        "reasoning": sum(r["reasoning_tokens"] or 0 for r in all_rows),
        "input": sum(r["input_tokens"] or 0 for r in all_rows),
        "src_edited": sum(1 for path in edited if not TEST_PATH_RE.search(path)),
        "tests_edited": sum(1 for path in edited if TEST_PATH_RE.search(path)),
        **diff_stats(os.path.join(trial_dir, "verifier", "agent.diff")),
    }
    out["reasoning_per_call"] = out["reasoning"] / max(len(all_rows), 1)
    for name, (a, b) in phases.items():
        out[name + "_steps"] = b - a
        out[name + "_out"] = tokens("output_tokens", a, b)
        out[name + "_reasoning"] = tokens("reasoning_tokens", a, b)
        out[name + "_tests"] = count("test", a, b)
        out[name + "_probes"] = count("probe", a, b)
        out[name + "_looks"] = count("look", a, b)
    return out


def load(run_dirs):
    trials = []
    for run in run_dirs:
        for chunk in sorted(glob.glob(os.path.join(run, "trial-*"))):
            audit = collections.defaultdict(list)
            for path in glob.glob(os.path.join(chunk, "audit-*.jsonl")):
                for line in open(path, encoding="utf-8", errors="replace"):
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    if row.get("status") != "success":
                        continue
                    harness = row.get("harness") or ""
                    job = (row.get("run_id") or "").removesuffix("-" + harness)
                    audit[(job, harness)].append(row)
            for rows in audit.values():
                rows.sort(key=lambda r: r.get("start_epoch") or 0)
            for arm, log in ARMS.items():
                for path in sorted(glob.glob(os.path.join(chunk, "jobs", "*", "*", "agent", log))):
                    trials.append(trial(os.path.dirname(path), arm, audit))
    return trials


FIELDS = [
    ("calls", "model calls"), ("out", "output tokens"), ("reasoning", "... of them reasoning"),
    ("reasoning_per_call", "reasoning tokens per call"), ("input", "input tokens"),
    ("first_input", "first request, tokens"), ("ctx_at_edit", "request at the first edit, tokens"),
    ("peak_input", "largest request, tokens"),
    ("first_edit", "step of the first source edit"),
    ("explore_steps", "explore: steps"), ("explore_out", "explore: output tokens"),
    ("explore_reasoning", "explore: reasoning tokens"), ("explore_looks", "explore: look calls"),
    ("explore_tests", "explore: test runs"), ("explore_probes", "explore: inline probes"),
    ("work_steps", "work: steps"), ("work_out", "work: output tokens"),
    ("work_tests", "work: test runs"), ("work_probes", "work: inline probes"),
    ("tail_steps", "tail: steps"), ("tail_out", "tail: output tokens"),
    ("tail_tests", "tail: test runs"), ("tail_probes", "tail: inline probes"),
    ("tail_looks", "tail: look calls"),
    ("edits", "source edit calls"), ("testedits", "edits of test files"),
    ("tests", "test runs"), ("probes", "inline probes"),
    ("src_edited", "source files edited (tool calls)"),
    ("tests_edited", "test files edited (tool calls)"),
    ("src_files", "diff: source files"), ("src_added", "diff: source lines added"),
    ("test_added", "diff: test lines added"), ("final_chars", "final message, chars"),
    ("missing", "hidden tests not passed"),
]


def table(title, pairs):
    print(f"\n{title} ({len(pairs)} tasks; mean per task, KaroX / DSH, ratio)")
    for key, label in FIELDS:
        cols = []
        for arm in ARMS:
            vals = [p[arm][key] for p in pairs if p[arm].get(key) is not None]
            cols.append(statistics.mean(vals) if vals else float("nan"))
        ratio = cols[0] / cols[1] if cols[1] else float("nan")
        print(f"  {label:36s} {cols[0]:>11.1f} {cols[1]:>11.1f} {ratio:6.2f}")
    solved = [sum(1 for p in pairs if p[arm]["reward"] == 1.0) for arm in ARMS]
    wrote = [sum(1 for p in pairs if p[arm]["tests_edited"]) for arm in ARMS]
    print(f"  {'solved':36s} {solved[0]:>11d} {solved[1]:>11d}")
    print(f"  {'trials that edited a test file':36s} {wrote[0]:>11d} {wrote[1]:>11d}")


def main():
    by_task = collections.defaultdict(dict)
    for t in load([a for a in sys.argv[1:] if not a.startswith("--")]):
        by_task[t["task"]][t["arm"]] = t
    pairs = [p for p in by_task.values() if len(p) == len(ARMS)]
    # A trial that ended on a provider error in its first steps says nothing about the CLI.
    valid = [p for p in pairs if all(p[arm]["steps"] > 5 for arm in ARMS)]
    k_arm, d_arm = ARMS
    if "--tasks" in sys.argv:
        print("task | solved K/D | calls | first edit step | steps after the last edit | "
              "tests | probes | test-file edits | output k | diff: source files (+lines) | "
              "diff: test lines | hidden tests missed")
        for p in sorted(valid, key=lambda p: p[k_arm]["task"]):
            k, d = p[k_arm], p[d_arm]

            def both(key):
                return f"{k.get(key)}/{d.get(key)}"

            print(" | ".join([
                k["task"][:34], both("reward"), both("calls"), both("first_edit"),
                both("tail_steps"), both("tests"), both("probes"), both("testedits"),
                f"{k['out'] / 1000:.1f}/{d['out'] / 1000:.1f}",
                f"{k.get('src_files')}(+{k.get('src_added')})/"
                f"{d.get('src_files')}(+{d.get('src_added')})",
                both("test_added"), both("missing")]))

    def solved(p, arm):
        return p[arm]["reward"] == 1.0

    table("All valid tasks", valid)
    table("Tasks DSH solved and KaroX did not",
          [p for p in valid if solved(p, d_arm) and not solved(p, k_arm)])
    table("Tasks KaroX solved and DSH did not",
          [p for p in valid if solved(p, k_arm) and not solved(p, d_arm)])
    table("Tasks both solved", [p for p in valid if solved(p, k_arm) and solved(p, d_arm)])
    table("KaroX's five dearest tasks (output tokens)",
          sorted(valid, key=lambda p: -p[k_arm]["out"])[:5])
    table("Short tasks (both arms <= 60 calls)",
          [p for p in valid if max(p[arm]["calls"] for arm in ARMS) <= 60])


if __name__ == "__main__":
    main()
