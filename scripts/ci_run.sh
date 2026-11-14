#!/usr/bin/env bash
# One GitHub Actions job: ONE task x ONE arm x N attempts in parallel.
#   ci_run.sh <task_name> <task_no 1..12> <arm: karox5|opencode_v2|deepseek_harness> <attempts> <tag>
# Same plumbing as the local HARD12 stand: litellm gateway :4100 (W&B, one pinned
# model and sampling profile), unwrap :4110, in-container relay, Harbor egress
# allowlist = docker bridge only. WANDB_API_KEY is given to litellm only.
set -euo pipefail
TASKDIR=$1; TASK=$(basename "$1"); N=$2; ARM=$3; ATT=$4; TAG=$5
ROOT=${GITHUB_WORKSPACE:-$(cd "$(dirname "$0")/.." && pwd)}
WORK=${RUNNER_TEMP:-/tmp}/h12
mkdir -p "$WORK/jobs" "$WORK/logs" "$WORK/tasks" "$WORK/audit/context"
RACE_GATEWAY_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(24))')
export RACE_GATEWAY_KEY
echo "::add-mask::$RACE_GATEWAY_KEY"
# UPSTREAM=synthetic swaps only the provider serving the same model (same profile).
if [ "${UPSTREAM:-wandb}" = synthetic ]; then
  [ -n "${SYNTHETIC_API_KEY:-}" ] || { echo "no SYNTHETIC_API_KEY secret"; exit 1; }
  CFG=litellm.hard12.synthetic.yaml; PROF=inference_profile_hard12_synthetic.json; KEYVAR=SYNTHETIC_API_KEY; KEYVAL=$SYNTHETIC_API_KEY
elif [ "${UPSTREAM:-wandb}" = runcrate ]; then
  [ -n "${RUNCRATE_API_KEY:-}" ] || { echo "no RUNCRATE_API_KEY secret"; exit 1; }
  CFG=litellm.hard12.runcrate.yaml; PROF=inference_profile_hard12_runcrate.json; KEYVAR=RUNCRATE_API_KEY; KEYVAL=$RUNCRATE_API_KEY
else
  [ -n "${WANDB_API_KEY:-}" ] || { echo "no WANDB_API_KEY secret"; exit 1; }
  CFG=litellm.hard12.yaml; PROF=inference_profile_hard12.json; KEYVAR=WANDB_API_KEY; KEYVAL=$WANDB_API_KEY
fi
(
  cd "$ROOT/gateway"
  env -i PATH="$PATH" HOME="$HOME" "$KEYVAR=$KEYVAL" \
    HARNESS_RACE_GATEWAY_KEY="$RACE_GATEWAY_KEY" HARNESS_RACE_AUDIT_DIR="$WORK/audit" \
    HARNESS_RACE_PROFILE="$ROOT/config/$PROF" LITELLM_TELEMETRY=False \
    nohup litellm --config "$CFG" --host 0.0.0.0 --port 4100 --num_workers 1 \
    >"$WORK/logs/litellm.log" 2>&1 &
)
unset WANDB_API_KEY SYNTHETIC_API_KEY RUNCRATE_API_KEY KEYVAL
(cd "$ROOT" && nohup python3 gateway/race_unwrap.py 4110:127.0.0.1:4100 >"$WORK/logs/unwrap.log" 2>&1 &)
health() { python3 -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:4100/health/liveliness',timeout=5)" 2>/dev/null; }
for _ in $(seq 1 120); do health && break; sleep 2; done
health || { echo "GATEWAY_FAIL"; tail -50 "$WORK/logs/litellm.log"; exit 1; }
LABEL="hard12-$TAG-$(printf '%02d' "$N")-$TASK"
printf '{"run_id": "%s-%s", "task_id": "%s"}\n' "$LABEL" "$ARM" "$TASK" > "$WORK/audit/context/$ARM.json"
cp -r "$ROOT/$TASKDIR" "$WORK/tasks/$TASK"
export PYTHONPATH="$ROOT/harbor_agents"
HARD12_ARMS="$ARM" HARD12_ATTEMPTS="$ATT" \
  HARD12_KARO_WHEEL="$ROOT/wheels/karox_runtime-5.0.0-py3-none-any.whl" \
  python3 "$ROOT/scripts/hard12_render_job.py" "$TASKDIR" "$WORK/tasks/$TASK" "$WORK/job.json"
echo "== $LABEL start $(date -u +%FT%TZ)"
harbor run --config "$WORK/job.json" --job-name "$LABEL" -o "$WORK/jobs" -q || echo "harbor rc=$?"
echo "== $LABEL done $(date -u +%FT%TZ)"
grep -rh "" "$WORK/jobs/$LABEL"/*/verifier/reward.txt 2>/dev/null || true
