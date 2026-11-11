"""Build one HARD12 Harbor task from a fresh (post-2026-10-18) RED/GREEN-validated PR.

    python3 make_hard12_task.py <fresh_ordered.json> <validation.jsonl> <repo#pr> <task_name> <validated Dockerfile>

Differences from make_swer_task.py (SWE-rebench rows):
* the environment image is the repo's SWE-rebench image REBUILT at the fresh
  base commit (only that commit is fetched, so no future objects exist), then
  all refs/remotes/reflog are stripped exactly like the race tasks;
* instruction = shared preamble + the ISSUE title/body (what a developer saw),
  never the PR description;
* F2P/P2P come from our own Docker RED/GREEN run (validate.py);
* the container relay points at the HARD12 gateway (docker bridge :4110).
"""
from __future__ import annotations

import json
import shlex
import shutil
import sys
from pathlib import Path

RACE = Path(__file__).resolve().parents[1]
OUT_ROOT = RACE / "hard12_tasks"
TEMPLATE = RACE / "templates"
PY = "/usr/local/bin/python"
PYTEST = "python -m pytest --no-header -rA --tb=no --color=no -p no:cacheprovider"

ENTRYPOINT = """#!/bin/bash
# HARD12 plumbing, identical for every arm: model traffic leaves the container
# only through this loopback relay -> HARD12 gateway (docker bridge :4110).
GW=$(python3 -c "r = open('/proc/net/route').read().splitlines(); l = [x.split() for x in r if x.split() and x.split()[1] == '00000000'][0]; print('.'.join(str(int(l[2][i:i+2], 16)) for i in (6, 4, 2, 0)))")
PY=$(command -v /opt/conda/bin/python || command -v python3)
"$PY" /opt/karo_relay.py 14000 "$GW:4110" >/tmp/relay_llm.log 2>&1 &
exec "$@"
"""


def main() -> int:
    ordered, results, key, name, validated_dockerfile = sys.argv[1:6]
    cand = next(c for c in json.load(open(ordered, encoding="utf-8")) if f"{c['repo']}#{c['pr']}" == key)
    val = next(json.loads(l) for l in open(results) if json.loads(l)["key"] == key)
    if not val.get("valid"):
        raise SystemExit(f"{key} did not pass RED/GREEN")
    base, image = cand["base"], cand["image"]
    # Only real pytest node ids (drop -rA separator/summary artifacts).
    f2p = [t for t in val["f2p"] if "::" in t]
    p2p = [t for t in val["p2p"] if "::" in t]
    files = val["test_files"]
    patch_files = [l.split()[2][2:] for l in cand["test_patch"].splitlines() if l.startswith("diff --git ")]
    out = OUT_ROOT / name
    if out.exists():
        raise SystemExit(f"refuse overwrite: {out}")
    (out / "environment").mkdir(parents=True)
    (out / "tests").mkdir()
    shutil.copyfile(OUT_ROOT / "_plumbing" / "karo_relay.py", out / "environment" / "karo_relay.py")
    (out / "environment" / "entrypoint.sh").write_text(ENTRYPOINT, encoding="utf-8", newline="\n")
    # EXACT slim recipe that passed RED/GREEN (validate_slim.py): python:<ver>-slim
    # + the repo at the fresh base commit (the only commit in .git) + install.
    recipe = Path(validated_dockerfile).read_text(encoding="utf-8").rstrip() + "\n"
    (out / "environment" / "Dockerfile").write_text(recipe + f"""RUN cd /testbed \\
 && git config --global --add safe.directory /testbed \\
 && (git remote | xargs -r -n1 git remote remove) \\
 && (git for-each-ref --format='%(refname)' | grep -v '^refs/heads/hard12-base$' | xargs -r -n1 git update-ref -d) \\
 && git reflog expire --expire=now --all \\
 && git gc --prune=now -q \\
 && test "$(git rev-list --all | wc -l)" = "1" \\
 && test "$(git rev-parse HEAD)" = "{base}"
COPY karo_relay.py /opt/karo_relay.py
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh
WORKDIR /testbed
ENTRYPOINT ["/opt/entrypoint.sh"]
""", encoding="utf-8", newline="\n")
    (out / "tests" / "test_patch.diff").write_text(cand["test_patch"], encoding="utf-8", newline="\n")
    (out / "tests" / "expected_passed.txt").write_text("\n".join(f2p + p2p) + "\n", encoding="utf-8", newline="\n")
    run_files = " ".join(shlex.quote(f) for f in files)
    (out / "tests" / "test.sh").write_text(f"""#!/bin/bash
# HARD12 grader for {key}: F2P ({len(f2p)}) must pass (they failed at base),
# P2P ({len(p2p)}) must still pass. Hidden test patch is applied only here.
set -u
cd /testbed
git config --global --add safe.directory /testbed
# Keep the agent's final change for analysis (grading does not read it).
mkdir -p /logs/verifier; (git add -A -N . && git diff HEAD) > /logs/verifier/agent.diff 2>/dev/null; git reset -q 2>/dev/null
TEST_FILES=$(grep -E '^diff --git a/' /tests/test_patch.diff | sed -E 's#^diff --git a/(.+) b/.*$#\\1#')
git checkout {base} -- $TEST_FILES >/dev/null 2>&1
for f in $TEST_FILES; do git cat-file -e {base}:"$f" 2>/dev/null || rm -f "$f"; done
git apply -v /tests/test_patch.diff >/tmp/test_patch.log 2>&1 || patch --batch -f -p1 -i /tests/test_patch.diff >>/tmp/test_patch.log 2>&1 || true
source /opt/conda/bin/activate testbed 2>/dev/null || true
timeout 900 {PYTEST} {run_files} > /tmp/eval_tests.log 2>&1 || true
FAIL=$(python3 - <<'PYEOF'
# Fixed-string match; pytest -rA truncates parametrised ids at the first space,
# so an id with "[" but no closing "]" is matched as a line prefix.
lines = open("/tmp/eval_tests.log", errors="replace").read().splitlines()
missing = []
for i in (x for x in open("/tests/expected_passed.txt").read().splitlines() if "::" in x):
    p = "PASSED " + i
    trunc = "[" in i and not i.endswith("]")
    if not any(l.startswith(p) and (trunc or l[len(p):] in ("",) or l[len(p):].startswith(" ")) for l in lines):
        missing.append(i)
open("/tmp/eval_missing.log", "w").write("".join("NOT PASSED: " + m + chr(10) for m in missing))
print(1 if missing else 0)
PYEOF
)
mkdir -p /logs/verifier
echo $([ "$FAIL" -eq 0 ] && echo 1 || echo 0) > /logs/verifier/reward.txt
cp -f /tmp/eval_tests.log /tmp/test_patch.log /tmp/eval_missing.log /logs/verifier/ 2>/dev/null || true
exit 0
""", encoding="utf-8", newline="\n")
    toml = (TEMPLATE / "task.toml").read_text(encoding="utf-8").replace("\r\n", "\n")
    toml = toml.replace('name = "karox/swe-rebench-1"', f'name = "hard12/{name}"')
    toml = toml.replace("SWE-rebench instance 0b01001001__spectree-64 (frozen)",
                        f"HARD12 fresh task {key} (PR merged {cand['merged'][:10]}, post-checkpoint)")
    toml = toml.replace("[agent]\ntimeout_sec = 1800.0", "[agent]\ntimeout_sec = 3600.0")
    toml = toml.replace("build_timeout_sec = 600.0", "build_timeout_sec = 2400.0")
    (out / "task.toml").write_text(toml, encoding="utf-8", newline="\n")
    preamble = (TEMPLATE / "instruction_preamble.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    issue = cand["problem_statement"] or {}
    (out / "instruction.md").write_text(
        preamble + "\n" + (issue.get("title") or "") + "\n\n" + (issue.get("body") or "") + "\n",
        encoding="utf-8", newline="\n")
    # Generic and identical for every task: nothing derived from the hidden
    # tests (their paths/dirs would leak which tests grade the run). The other
    # CLIs get no verification hint at all; KaroX gets only "pytest / python".
    (out / "karo_options.json").write_text(json.dumps({
        "task_dir": "/testbed", "verify_command": [[PY, "-m", "pytest", "*"], [PY, "*"]],
    }, indent=2) + "
", encoding="utf-8", newline="
")
    (out / "README.md").write_text(
        f"# HARD12 task `{name}`\n\n| item | value |\n|---|---|\n| source | {cand['url']} |\n"
        f"| issue | #{cand['issue']} (created {cand['issue_created'][:10]}) |\n| PR created / merged | "
        f"{cand['created'][:10]} / {cand['merged'][:10]} |\n| base | `{base}` |\n| image base | `{image}` |\n"
        f"| F2P / P2P | {len(f2p)} / {len(p2p)} |\n| test files | {', '.join(files)} |\n\n"
        "Fresh task: the fix post-dates the DeepSeek-V4.1-Flash-1017 checkpoint; agents have no "
        "internet during the agent phase (allowlist = docker bridge only).\n", encoding="utf-8", newline="\n")
    print(f"wrote {out} f2p={len(f2p)} p2p={len(p2p)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
