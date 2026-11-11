#!/bin/bash
# HARD12 grader for SpikeInterface/spikeinterface#4921: F2P (6) must pass (they failed at base),
# P2P (18) must still pass. Hidden test patch is applied only here.
set -u
cd /testbed
git config --global --add safe.directory /testbed
# Keep the agent's final change for analysis (grading does not read it).
mkdir -p /logs/verifier; (git add -A -N . && git diff HEAD) > /logs/verifier/agent.diff 2>/dev/null; git reset -q 2>/dev/null
TEST_FILES=$(grep -E '^diff --git a/' /tests/test_patch.diff | sed -E 's#^diff --git a/(.+) b/.*$#\1#')
git checkout 4e28d878e240753573ea3e2a42cdf6267015314b -- $TEST_FILES >/dev/null 2>&1
for f in $TEST_FILES; do git cat-file -e 4e28d878e240753573ea3e2a42cdf6267015314b:"$f" 2>/dev/null || rm -f "$f"; done
git apply -v /tests/test_patch.diff >/tmp/test_patch.log 2>&1 || patch --batch -f -p1 -i /tests/test_patch.diff >>/tmp/test_patch.log 2>&1 || true
source /opt/conda/bin/activate testbed 2>/dev/null || true
timeout 900 python -m pytest --no-header -rA --tb=no --color=no -p no:cacheprovider src/spikeinterface/core/tests/test_basesorting.py src/spikeinterface/core/tests/test_numpy_extractors.py > /tmp/eval_tests.log 2>&1 || true
FAIL=0
while IFS= read -r id; do
  [ -n "$id" ] || continue
  grep -qE "^PASSED $(printf '%s' "$id" | sed 's/[][\.*^$/]/\\&/g')( |$)" /tmp/eval_tests.log || { FAIL=1; echo "NOT PASSED: $id" >>/tmp/eval_missing.log; }
done </tests/expected_passed.txt
mkdir -p /logs/verifier
echo $([ "$FAIL" -eq 0 ] && echo 1 || echo 0) > /logs/verifier/reward.txt
cp -f /tmp/eval_tests.log /tmp/test_patch.log /tmp/eval_missing.log /logs/verifier/ 2>/dev/null || true
exit 0
