#!/bin/bash
# HARD12 grader for PyCQA/isort#2757: F2P (2) must pass (they failed at base),
# P2P (130) must still pass. Hidden test patch is applied only here.
set -u
cd /testbed
git config --global --add safe.directory /testbed
# Keep the agent's final change for analysis (grading does not read it).
mkdir -p /logs/verifier; (git add -A -N . && git diff HEAD) > /logs/verifier/agent.diff 2>/dev/null; git reset -q 2>/dev/null
TEST_FILES=$(grep -E '^diff --git a/' /tests/test_patch.diff | sed -E 's#^diff --git a/(.+) b/.*$#\1#')
git checkout 1d60803ae4db8ba77c4f1f93f9244c6478c3bf63 -- $TEST_FILES >/dev/null 2>&1
for f in $TEST_FILES; do git cat-file -e 1d60803ae4db8ba77c4f1f93f9244c6478c3bf63:"$f" 2>/dev/null || rm -f "$f"; done
git apply -v /tests/test_patch.diff >/tmp/test_patch.log 2>&1 || patch --batch -f -p1 -i /tests/test_patch.diff >>/tmp/test_patch.log 2>&1 || true
source /opt/conda/bin/activate testbed 2>/dev/null || true
timeout 900 python -m pytest --no-header -rA --tb=no --color=no -p no:cacheprovider tests/unit/test_regressions.py > /tmp/eval_tests.log 2>&1 || true
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
