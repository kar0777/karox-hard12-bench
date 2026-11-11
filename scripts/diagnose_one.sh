#!/usr/bin/env bash
# Re-grade saved final diffs of one task with tracebacks (--tb=short), plus the
# upstream gold patch as a solvability control. Grading itself is unchanged.
#   diagnose_one.sh <task_no>
set -uo pipefail
N=$1
ROOT=${GITHUB_WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}
OUT=$ROOT/out/$N; mkdir -p "$OUT"
read -r KEY SLUG < <(sed -n "${N}p" "$ROOT/data/night_tasks.txt")
TASK=$ROOT/hard12_tasks/h12-${SLUG:0:40}
python3 - "$KEY" > "$ROOT/data/diag/$N/gold.diff" <<'EOF'
import json, sys
c = [x for x in json.load(open("data/candidates2.json")) if f"{x['repo']}#{x['pr']}" == sys.argv[1]]
print(c[0]["gold_patch"] if c else "", end="")
EOF
docker build -q -t diag "$TASK/environment" >/dev/null || { echo "build failed" > "$OUT/error.txt"; exit 0; }
sed 's/--tb=no/--tb=short/' "$TASK/tests/test.sh" > "$OUT/test_tb.sh"
for d in "$ROOT/data/diag/$N"/*.diff; do
  arm=$(basename "$d" .diff)
  docker rm -f diag1 >/dev/null 2>&1
  docker run -d --name diag1 --entrypoint sleep diag infinity >/dev/null
  docker cp "$TASK/tests" diag1:/tests
  docker cp "$OUT/test_tb.sh" diag1:/tests/test_tb.sh
  docker cp "$d" diag1:/tmp/agent.diff
  docker exec diag1 bash -c 'cd /testbed && (git apply /tmp/agent.diff 2>/tmp/apply.log || patch -p1 -f < /tmp/agent.diff >>/tmp/apply.log 2>&1); bash /tests/test_tb.sh' >/dev/null 2>&1
  docker cp diag1:/tmp/eval_tests.log "$OUT/$arm.tests.log" 2>/dev/null
  docker cp diag1:/tmp/eval_missing.log "$OUT/$arm.missing.log" 2>/dev/null
  docker cp diag1:/tmp/apply.log "$OUT/$arm.apply.log" 2>/dev/null
  echo "$arm missing=$(grep -c 'NOT PASSED' "$OUT/$arm.missing.log" 2>/dev/null)"
done
docker rm -f diag1 >/dev/null 2>&1
